#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory, jsonify, abort
import os
import hmac
import hashlib
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = '/home/dev/files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'abc12345'

def generate_hash(filename, secret_key, date):
    data = f"{filename}{date}{secret_key}"
    return hashlib.sha256(data.encode()).hexdigest()

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def list_files():
    #files = os.listdir(app.config['UPLOAD_FOLDER'])
    #return jsonify(files=files)
    return render_template_string(open('/home/dev/data/uploader.html').read())

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"OK\n"

@app.route('/d/<hashing>/<filename>')
def uploaded_file(hashing, filename):
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    expected_hash = generate_hash(filename, app.config['SECRET_KEY'], today_date)[:8]
    
    if hmac.compare_digest(hashing, expected_hash):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=8004)
