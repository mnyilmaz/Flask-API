import joblib
import evaluate
import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import pipeline
from transformers import create_optimizer
from transformers import AutoTokenizer, DataCollatorWithPadding
from transformers import TFAutoModelForSequenceClassification
from transformers.keras_callbacks import KerasMetricCallback
from transformers.keras_callbacks import PushToHubCallback

'''
This training file includes 'Text-Classification' to attain relevant tag for the relevant ticket issue.
Data file 'step11.csv' includes 3 main column: 
    1) Title
    2) Description
    3) Values
    
Related to descriptions, if issue corresponds to the relevant description, value must be attained as a tag.

Tag Structure
  Report a BUG
    - Value: 0
  Suggest a new future
    - Value: 1
  Suggest improvement
    - Value: 2
  Technical support
    - Value: 3
      
'''

# Import and check the dataset
issue = pd.read_csv('step11.csv', encoding='iso-8859-9')
print(f"Title: {issue['Title'][0]}\n")
print(f"Description: {issue['Description'][0]}\n")
print(f"Value: {issue['Values'][0]}\n")

# Load DistilBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


# Preprocess function to tokenize text and truncate sequences
def preprocess_function(description):
    return tokenizer(description, truncation=True)


# Apply the preprocessing function to the 'Description' column
tokenized_issue = issue['Description'].apply(preprocess_function)

# Form batch of examples
data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="tf")

# Importing evaluation to check accuracy
accuracy = evaluate.load("accuracy")


# Function that passes predictions and labels to compute to calculate the accuracy
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)


# Tag mapping
id2tag = {0: "Report a BUG", 1: "Suggest a new feature", 2: "Suggest improvement", 3: "Technical support"}
tag2id = {"Report a BUG": 0, "Suggest a new feature": 1, "Suggest improvement": 2, "Technical support": 3}

# Training hyperparameters
batch_size = 16
num_epochs = 5
batches_per_epoch = len(tokenized_issue["train"]) // batch_size
total_train_steps = int(batches_per_epoch * num_epochs)
optimizer, schedule = create_optimizer(init_lr=2e-5, num_warmup_steps=0, num_train_steps=total_train_steps)

# Load DistilBERT
model = TFAutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2, id2label=id2tag, label2id=tag2id
)

# Convert datasets to the tf.data.Dataset format

tf_train_set = model.prepare_tf_dataset(
    tokenized_issue["train"],
    shuffle=True,
    batch_size=16,
    collate_fn=data_collator,
)

tf_validation_set = model.prepare_tf_dataset(
    tokenized_issue["test"],
    shuffle=False,
    batch_size=16,
    collate_fn=data_collator,
)

# Configure the model for training with compile
model.compile(optimizer=optimizer)

# Pass compute_metrics function to KerasMetricCallback
metric_callback = KerasMetricCallback(metric_fn=compute_metrics, eval_dataset=tf_validation_set)

# Specify where to push the model and tokenizer into PushToHubCallback
push_to_hub_callback = PushToHubCallback(
    output_dir="kara_v01",
    tokenizer=tokenizer,
)

# Bundling callbacks
callbacks = [metric_callback, push_to_hub_callback]

# How to train your model finally
model.fit(x=tf_train_set, validation_data=tf_validation_set, epochs=3, callbacks=callbacks)

# Now test is
text = "cognos dk eşlemedeki uyumsuzluk sebebi yedeğinin alınmasını talep eder"

classifier = pipeline("sentiment-analysis", model="stevhliu/kara_v01")
classifier(text)
