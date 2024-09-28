from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Hi there!<h1>'


@app.route('/user/<name>')
def user(name):
    return f"hi {name}"


if __name__ == '__main__':
    app.run(debug=True, port=5005)