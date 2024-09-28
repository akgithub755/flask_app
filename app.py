from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Hi there!<h1>'


@app.route('/user/<name>')
def user(name):
    return f"hi {name}"


@app.route('/user-agent')
def index():
    user_agent = request.headers.get('User-Agent')
    return f"your broswer is {user_agent}"


if __name__ == '__main__':
    app.run(debug=True, port=5005)