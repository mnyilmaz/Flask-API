from flask import Flask, request, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, template_folder='../templates')
dir_temp_home = 'home.html'
dir_temp_tag = 'tag.html'

# Set a secret key
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize CSRF protection
csrf = CSRFProtect(app)


class IssueForm(FlaskForm):
    issue = StringField('Issue')


# List to store issues (replace this with database integration if needed)
issues_list = []


@app.route("/")
def home():
    return render_template(dir_temp_home), 200


@app.route('/tag.html', methods=['POST', 'GET'])
def tag():
    form = IssueForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the issue text from the form and add it to the issues_list
            issue_text = form.issue.data
            issues_list.append(issue_text)

            # Redirect to the same page after handling the POST request
            return redirect('/tag.html')

    # Pass the list of issues to the template
    return render_template(dir_temp_tag, form=form, issues_list=issues_list)


if __name__ == '__main__':
    app.run(debug=True)
