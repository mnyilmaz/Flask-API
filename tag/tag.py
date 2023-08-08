import requests
from flask_mail import Mail, Message
from flask import Flask, request, jsonify
from text_tag_classification import new_prediction


# Initializing the Flask app and template folder
app = Flask(__name__, template_folder='../templates')

# Set a secret key for CSRF Token implementation, otherwise it might raise an error
app.config['SECRET_KEY'] = 'secret_key'

# Mail configuration
app.config['DEBUG'] = False  # To suppress flask_mail console output turn into 'True'
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


def send_mail_to_user(title, issue, tag):
    msg = Message(f"About your issue: '{title}';",
                  recipients=['temp@mail.com'])
    msg.body = f"Dear user; \n\n Related to your issue: \n '{issue}' \n '{tag}' tag has attained."
    mail.send(msg)
    print(msg.body)
    return 'Sent'


# Home route
@app.route("/")
def home():
    return jsonify({'success': 'Home Page'}), 200


# Main route
@app.route('/tagAPI', methods=['POST', 'GET'])
def tag():
    try:
        data = request.get_json()
        title = data['title']
        issue = data['issue']
        title = str(title)
        issue = str(issue)

    except Exception as e:
        return jsonify({'error': 'Invalid JSON data'}), 400

    prediction = new_prediction(title, issue)

    if prediction == 0:
        tag_text = 'Report a BUG'
        send_mail_to_user(title, issue, tag_text)
    elif prediction == 1:
        tag_text = 'Suggest a new feature'
        send_mail_to_user(title, issue, tag_text)
    elif prediction == 2:
        tag_text = 'Suggest improvement'
        send_mail_to_user(title, issue, tag_text)
    else:
        tag_text = 'Technical support'
        send_mail_to_user(title, issue, tag_text)
    print(prediction)

    return jsonify({'tag': tag_text})


if __name__ == '__main__':
    app.run(debug=True)
