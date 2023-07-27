import joblib
import numpy as np
import pandas as pd
from wtforms import StringField
from flask_mail import Mail, Message
from wtforms.csrf.session import SessionCSRF
from flask_wtf import CSRFProtect, FlaskForm
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from flask import Flask, request, render_template, redirect
from tensorflow.keras.preprocessing.sequence import pad_sequences


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

# Initialize CSRF protection but usage is not necessary
csrf = CSRFProtect(app)
csrf.init_app(app)


# Normally form usage is not needed but for test environment i've added
class IssueForm(FlaskForm):
    issue = StringField('Issue')
    tag = StringField('Tag')


# List to store issues
issues_list = []
tags_list = []

# Load the trained model from disk for inference
loaded_model = load_model('trained_model.h5')

# Tokenizer and other necessary variables
max_features = 2000
max_seq_length = 100
tokenizer = Tokenizer(num_words=max_features, split=' ')
le = joblib.load('label_encoder.pkl')


# Normally this def was inside training.py, but in every call it was running the training over and over again
def predict_category(text, tokenizer, le, max_seq_length):
    text_seq = tokenizer.texts_to_sequences([text])
    text_padded = pad_sequences(text_seq, maxlen=max_seq_length)
    prediction = loaded_model.predict(text_padded)
    predicted_class = le.inverse_transform([np.argmax(prediction)])[0]
    return predicted_class


def reportBug(issue):
    msg = Message(f"About your issue: '{issue}';",
                  recipients=['temp@mail.com'])
    msg.body = "Dear user; \n\n Related to your issue 'Report a BUG' tag has attained."
    mail.send(msg)
    return 'Sent'


def suggestFeature(issue):
    msg = Message(f"About your issue: '{issue}';",
                  recipients=['temp@mail.com'])
    msg.body = "Dear user; \n\n Related to your issue 'Suggest a new future' tag has attained."
    mail.send(msg)
    return 'Sent'


def suggestImprovement(issue):
    msg = Message(f"About your issue: '{issue}';",
                  recipients=['temp@mail.com'])
    msg.body = "Dear user; \n\n Related to your issue 'Suggest improvement' tag has attained."
    mail.send(msg)
    return 'Sent'


def technicalSupport(issue):
    msg = Message(f"About your issue: '{issue}';",
                  recipients=['temp@mail.com'])
    msg.body = "Dear user; \n\n Related to your issue 'Technical support' tag has attained."
    mail.send(msg)
    return 'Sent'


# Home route
@app.route("/")
def home():
    return render_template(dir_temp_home), 200


# Main route
@app.route('/tag.html', methods=['POST', 'GET'])
def tag():
    form = IssueForm()

    if request.method == 'POST' and form.validate():
        # Get the issue text from the form and add it to the issues_list
        issue_text = form.issue.data
        tag_text = form.tag.data
        predicted_category = predict_category(issue_text, tokenizer, le, max_seq_length)
        print("Predicted category:", predicted_category)
        if predicted_category == 0:
            tag_text = 'Report a BUG'
            reportBug(issue_text)
        elif predicted_category == 1:
            tag_text = 'Suggest a new future'
            suggestFeature(issue_text)
        elif predicted_category == 2:
            tag_text = 'Suggest improvement'
            suggestImprovement(issue_text)
        else:
            tag_text = 'Technical support'
            technicalSupport(issue_text)
        # Store the issue and tag as a tuple in issues_list
        issues_list.append((issue_text, tag_text))

        # Redirect to the same page after handling the POST request
        return redirect('/tag.html')

    # Pass the list of issues to the template
    return render_template(dir_temp_tag, form=form, issues_list=issues_list)


if __name__ == '__main__':
    app.run(debug=True)
