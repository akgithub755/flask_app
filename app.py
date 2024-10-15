from flask import Flask, request, render_template, make_response,\
redirect, jsonify, Response
import os
import io
import sys
import time
from upload import process_excel_file  # import the function from upload.py


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


@app.route('/apple')
def apple():
    return redirect('https://www.apple.com/')


@app.route('/wbu')
def wbu():
    return render_template('wbu.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file and allowed_file(file.filename):
        file_path = os.path.join('', file.filename)
        file.save(file_path)
        
        return Response(stream_with_context(process_excel_file(file_path)), mimetype='text/plain')

    return 'Invalid file'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']

def stream_with_context(generator_func):
    """Helper function to yield log lines as the generator runs."""
    for log in generator_func:
        yield f"{log}\n"
        time.sleep(0.1)


if __name__ == '__main__':
    app.run(debug=True, port=5005)