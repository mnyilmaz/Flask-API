from flask import Flask, request, render_template, redirect
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField
from main import predict_category

app = Flask(__name__, template_folder='../templates')
dir_temp_home = 'home.html'
dir_temp_tag = 'tag.html'

# Set a secret key
app.config['SECRET_KEY'] = 'secret_key'

# Initialize CSRF protection
csrf = CSRFProtect(app)
csrf.init_app(app)


class IssueForm(FlaskForm):
    issue = StringField('Issue')
    tag = StringField('Tag')


# List to store issues (replace this with database integration if needed)
issues_list = []
tags_list = []


# Home route
@app.route("/")
def home():
    return render_template(dir_temp_home), 200


# Main route
@app.route('/tag.html', methods=['POST', 'GET'])
def tag():
    form = IssueForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the issue text from the form and add it to the issues_list
            issue_text = form.issue.data
            tag_text = form.tag.data
            predicted_category = predict_category(issue_text)
            print("Predicted category:", predicted_category)
            if predict_category == 0:
                tag_text = 'Report a BUG'
            elif predict_category == 1:
                tag_text = 'Suggest a new future'
            elif predict_category == 2:
                tag_text = 'Suggest Improvement'
            else:
                tag_text = 'Technical Support'
            issues_list.append((issue_text, tags_list[-1] if tags_list else ''))
            tags_list.append(tag_text)

            # Redirect to the same page after handling the POST request
            return redirect('/tag.html')

    # Pass the list of issues to the template
    return render_template(dir_temp_tag, form=form, issues_list=issues_list, tags_list=tags_list)


if __name__ == '__main__':
    app.run(debug=True)
