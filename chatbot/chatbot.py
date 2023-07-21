import random
import json
import pickle
import numpy as np
import tensorflow as tf
import os
import nltk
from flask import Flask, request, jsonify, render_template
from nltk.stem import WordNetLemmatizer

current_dir = os.path.dirname(os.path.abspath(__file__))
intents_file_path = os.path.join(current_dir, 'intents.json')
words_file_path = os.path.join(current_dir, 'words.pkl')
classes_file_path = os.path.join(current_dir, 'classes.pkl')
model_file_path = os.path.join(current_dir, 'chatbotmodel.h5')

lemmatizer = WordNetLemmatizer()
with open(intents_file_path, 'r') as intentFile:
    intents = json.load(intentFile)
with open(words_file_path, 'rb') as wordFile:
    words = pickle.load(wordFile)
with open(classes_file_path, 'rb') as classesFile:
    classes = pickle.load(classesFile)
model = tf.keras.models.load_model(model_file_path)


# Cleaning up the sentence func
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


# Indicate if there is word or not with full of list 1 and 0s
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
            # otherwise its automatically zero
    return np.array(bag)


# Predict func
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


# For chatting with Chatbot
def get_response(intents_list, intent_json):
    tag = intents_list[0]['intent']
    list_of_intents = intent_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    else:
        result = "Sorry, I didn't quite understand that."
    return result


# Defining the Flask app
app = Flask(__name__, template_folder='../templates')


@app.route("/")
def home():
    dir_temp = "index.html"
    return render_template(dir_temp)


@app.route("/api/chatbot", methods=['POST'])
def chatbot():
    # Content-Type header must be application/json otherwise error occurs
    if request.headers['Content-Type'] == 'application/json':
        try:
            # Get the JSON data and predict
            data = request.get_json()
            msg = data['msg']
            ints = predict_class(msg)
            res = get_response(ints, intents)

            return jsonify({'response': res})  # Return the response as JSON

        except Exception as e:
            return jsonify({'error': 'Invalid request data'}), 400
    else:
        return jsonify({'error': 'Invalid Content-Type'}), 400


if __name__ == '__main__':
    app.run(debug=True)
