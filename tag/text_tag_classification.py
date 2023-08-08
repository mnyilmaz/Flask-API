import re
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

# Obtaining the values .csv file
data = pd.read_csv('step11.csv', encoding='utf-8')
data.head()

# Rename columns
data.columns = ['title', 'issue', 'value']

'''
This parts are not necessarily to print out yet useful to understand process.

print(data.head())
print(f"Title: {data['title'][0]}")
print(f"Issue: {data['issue'][0]}")
print(f"Category: {data['value'][0]}")

# Check data shape
print(data.shape)

# Check value balance in the .csv file
data['value'].value_counts(normalize=True).plot(kind='bar')
plt.show()
'''

# Text preprocessing, at first run remove comment line then use the comment line again
#  nltk.download('all')


# Initialize lists
title = list(data['title'])
issue = list(data['issue'])
value = list(data['value'])

# Cleaning the title and issue column
lemmatizer = WordNetLemmatizer()


def clean(text):
    corpus = []
    for i in range(len(text)):
        r = re.sub('[^a-zA-ZçğıöşüÇĞİÖŞÜ]', ' ', text[i])
        r = r.lower()
        r = r.split()
        r = [word for word in r if word not in stopwords.words('turkish')]
        r = [lemmatizer.lemmatize(word) for word in r]
        r = ' '.join(r)
        corpus.append(r)
    return corpus


data['title'] = clean(title)
data['issue'] = clean(issue)
'''
print(data.head())  -> print to see the result, do not hesitate to print data.head() throughout the process
'''

# Label sets
X_title = data['title']
X_issue = data['issue']
X = X_title + ' ' + X_issue
y = data['value']

# Test and train arrangement %33 test, %66 train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123)

print('Training Data :', X_train.shape)  # Training Data: (1466, )
print('Testing Data : ', X_test.shape)  # Testing Data: (723, )

# Check for missing values in y_train
missing_values = pd.isnull(y_train)
print(f"Missing value count: {missing_values.sum()}")

# Drop down missing values
X_train = X_train[~missing_values]
y_train = y_train[~missing_values]

# Impute missing values with the mode (most common value)
mode_value = y_train.mode()[0]
y_train = y_train.fillna(mode_value)

# Convert the cleaned text into numeric features with the Bag of Words model (CountVectorizer)
cv = CountVectorizer()

X_train_cv = cv.fit_transform(X_train)
print(f"X_train shape: {X_train_cv.shape}")  # (1466, 4154)

# Training Logistic Regression model
lr = LogisticRegression()
lr.fit(X_train_cv, y_train)

# Transform X_test using CV
X_test_cv = cv.transform(X_test)

# Generate predictions
predictions = lr.predict(X_test_cv)
# print(predictions)

# Get predicted probabilities for each class
predicted_probabilities = lr.predict_proba(X_test_cv)

'''
print(f"Predicted Probabilities for Each Class: \n{predicted_probabilities}")
'''


def new_prediction(title, issue):
    new_title = clean([title])[0]
    new_issue = clean([issue])[0]
    new_data = new_title + ' ' + new_issue

    # As above, vectorize the new data using the same CountVectorizer
    new_data_cv = cv.transform([new_data])

    new_predictions = lr.predict(new_data_cv)
    new_predicted_probabilities = lr.predict_proba(new_data_cv)

    '''
    Printing 'New Predicted Value' and 'New Predicted Probabilities' is not necessary. In order to
    understand the output values for further research, observation of these values might be beneficial.
    '''
    print(f"New Predicted Value: {new_predictions[0]}")
    print(f"New Predicted Probabilities for Each Class: {new_predicted_probabilities}")

    return new_predictions[0]
