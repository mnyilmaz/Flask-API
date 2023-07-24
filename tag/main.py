import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from tensorflow.keras.utils import to_categorical

data = pd.read_csv('adim11.csv', encoding='iso-8859-9')

X = data['Description']
y = data['Values']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Title sütununu ekleyin
title = data['Title']
X_train_title, X_test_title, y_train_title, y_test_title = train_test_split(title, y, test_size=0.2, random_state=42)

# X_train ve X_test verilerine Title sütununu ekleyin
X_train = X_train.str.cat(X_train_title, sep=' Title: ')
X_test = X_test.str.cat(X_test_title, sep=' Title: ')

X_description = data['Description']
X_title = data['Title']
X = X_description + ' ' + X_title
y = data['Values']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


X_train = X_train.fillna(" ")
X_test = X_test.fillna(" ")

max_features = 2000
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(X_train.values)
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

max_seq_length = 100
X_train_padded = pad_sequences(X_train_seq, maxlen=max_seq_length)
X_test_padded = pad_sequences(X_test_seq, maxlen=max_seq_length)

le = LabelEncoder()
y_train_enc = le.fit_transform(y_train)
y_test_enc = le.transform(y_test)
num_classes = len(le.classes_)

y_train_one_hot = to_categorical(y_train_enc, num_classes=num_classes)
y_test_one_hot = to_categorical(y_test_enc, num_classes=num_classes)

#orijinal
embedding_dim = 128

model = Sequential()
model.add(Embedding(max_features, embedding_dim, input_length=max_seq_length))
model.add(SpatialDropout1D(0.4))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

batch_size = 32
epochs = 5

model.fit(
    X_train_padded, y_train_one_hot,
    epochs=epochs, batch_size=batch_size,
validation_data=(X_test_padded, y_test_one_hot),
verbose=1
)

score, accuracy = model.evaluate(X_test_padded, y_test_one_hot, batch_size=batch_size, verbose=1)
print("Test puanı: {:.4f}, accuracy: {:.4f}".format(score, accuracy))

def predict_category(text):
    text_seq = tokenizer.texts_to_sequences([text])
    text_padded = pad_sequences(text_seq, maxlen=max_seq_length)
    prediction = model.predict(text_padded)
    predicted_class = le.inverse_transform([np.argmax(prediction)])[0]
    return predicted_class

new_text = "kullanici giriş hatası murat arslan"
predicted_category = predict_category(new_text)
print("Tahmin edilen kategori:", predicted_category)
if predict_category == 0 :
    print('Report a BUG')
elif predict_category == 1 :
    print('Suggest a new future')
elif predict_category == 2 :
    print('Suggest Improvement')
else:
    print('Technical Support')