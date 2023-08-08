import numpy as np
import pandas as pd
import joblib, requests
from flask_mail import Mail, Message
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, request, render_template, redirect, jsonify


# Initializing the Flask app and template folder
app = Flask(__name__, template_folder='../templates')
dir_temp_home = 'home.html'
dir_temp_tag = 'tag.html'

# Set a secret key for CSRF Token implementation, otherwise it might raise an error
app.config['SECRET_KEY'] = 'secret_key'

# Mail configuration
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'  # Outlook: smtp-mail.outlook.com | Gmail: smtp.gmail | Hushmail: smtp.hushmail.com
app.config['MAIL_PORT'] = 587  # Outlook port: 587 or 993 | Gmail port: 465 | Hushmail port: 587 | Temp mail port: 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'example@outlook.com'  # This is a temp mail and default value is None
app.config['MAIL_PASSWORD'] = '****'  # Default value is None
app.config['MAIL_DEFAULT_SENDER'] = ('... from ...', 'example@outlook.com')
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

# Load the trained model from disk for inference
model = load_model('trained_model.h5')

# Tokenizer and other necessary variables
max_features = 2000
max_seq_length = 100
tokenizer = Tokenizer(num_words=max_features, split=' ')
le = joblib.load('label_encoder.pkl')


def send_mail_to_user(issue, tag):
    msg = Message(f"About your issue: '{issue}';",
                  recipients=['temp@mail.com'])
    msg.body = f"Dear user; \n\n Related to your issue {tag} tag has attained."
    mail.send(msg)
    print(msg.body)
    return 'Sent'


def predict_category(text):
    text_seq = tokenizer.texts_to_sequences([text])
    text_padded = pad_sequences(text_seq, maxlen=max_seq_length)
    prediction = model.predict(text_padded)
    predicted_class = le.inverse_transform([np.argmax(prediction)])[0]
    return predicted_class


# Home route
@app.route("/")
def home():
    return jsonify({'success': 'Home Page'}), 200


# Main route
@app.route('/tagAPI', methods=['POST', 'GET'])
def tag():
    try:
        data = request.get_json()
        description = data['description']
        description = str(description)

    except Exception as e:
        return jsonify({'error': 'Invalid JSON data'}), 400

    predicted_class = predict_category(description)

    if predicted_class == 0:
        tag_text = 'Report a BUG'
        send_mail_to_user(description, tag_text)
    elif predicted_class == 1:
        tag_text = 'Suggest a new future'
        send_mail_to_user(description, tag_text)
    elif predicted_class == 2:
        tag_text = 'Suggest improvement'
        send_mail_to_user(description, tag_text)
    else:
        tag_text = 'Technical support'
        send_mail_to_user(description, tag_text)
    print(predicted_class)

    return jsonify({'tag': tag_text})


if __name__ == '__main__':
    app.run(debug=True)
