from flask import Flask, request, jsonify
import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer
from chatbot.chatbot import predict_class, get_response
lemmatizer = WordNetLemmatizer()


# chat initialization
model = load_model("chatbot/chatbot_model.h5")
intents = json.loads(open("chatbot/intents.json").read())
words = pickle.load(open("chatbot/words.pkl", "rb"))
classes = pickle.load(open("chatbot/classes.pkl", "rb"))

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    # checks is a user has given a name, in order to give a personalized feedback
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg)
        res1 = get_response(ints, intents)
        res = res1.replace("{n}", name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg)
        res1 = get_response(ints, intents)
        res = res1.replace("{n}", name)
    # if no name is passed execute normally
    else:
        ints = predict_class(msg)
        res = get_response(ints, intents)
    return res


if __name__ == '__main__':
    app.run()
