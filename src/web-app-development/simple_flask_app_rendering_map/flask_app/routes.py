from flask import render_template, json
from flask_app import app
import os

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Southwark'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Caesar Salad'},
            'body': 'Yum, these dublin bikes taste delicious!'
        }
    ]

    filename = os.path.join(app.static_folder, 'static.json')
    with open(filename) as bikes:
        data = json.load(bikes)
    return render_template('index.html', title='Home', user=user, posts=posts, data=data)
