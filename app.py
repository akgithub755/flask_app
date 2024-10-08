from flask import Flask, request, render_template, make_response
from flask_bootstrap import Bootstrap
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/user-agent')
def index():
    user_agent = request.headers.get('User-Agent')
    return f"your broswer is {user_agent}"


@app.route('/home')
def a1():
    response = make_response('<h1>This document carries a cookie</h1>')
    response.set_cookie('answer', '42')
    return response


bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True, port=5005)