from flask import render_template, json
from flask_app import app
import os

@app.route('/')
@app.route('/index')
def index():
    filename = os.path.join(app.static_folder, 'placeholder.json')
    with open(filename) as placeholder_data:
        data = json.load(placeholder_data)
    return render_template('index.html', title='Home', data=data)
