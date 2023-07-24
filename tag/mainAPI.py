from flask import Flask, request, jsonify, render_template

# from main import predict_category


# Defining the Flask app
app = Flask(__name__, template_folder='../templates')
dir_temp_home = 'home.html'
dir_temp_tag = 'issue.html'


# Home route
@app.route("/")
def home():
    return render_template(dir_temp_home)


# Tag route
@app.route('/tag.html', methods=['POST', 'GET'])
def tag():
    if request.method == 'GET':
        return render_template(dir_temp_tag), 200

    if request.method == 'POST':
        pass



if __name__ == '__main__':
    app.run(debug=True)
