import random
import json
import os
from flask import Flask, request, jsonify, render_template
from nltk.stem import WordNetLemmatizer

# Defining the Flask app
app = Flask(__name__, template_folder='../templates')


@app.route("/")
def home():
    dir_temp = "index.html"
    return render_template(dir_temp)

if __name__ == '__main__':
    app.run(debug=True)

