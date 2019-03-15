from flask import Flask, render_template, url_for, g, jsonify
from flask_app import app
import os
import config
import simplejson as json
import pymysql.cursors

def connect_to_database():
    try:
        connection = pymysql.connect(
            host=config.rds_host,
            user=config.rds_user,
            password=config.rds_password,
            db=config.rds_development_database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    # Make this exception actually work
    except:
        print("Unable to connect to database: {}".format(err))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/index')
def index():
    filename = os.path.join(app.static_folder, 'placeholder.json')
    with open(filename) as placeholder_data:
        data = json.load(placeholder_data)
    return render_template('index.html', title='Home', data=data, map_key=config.map_url)

@app.route("/stations")
def get_stations():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dublin_bikes_static")
        data = cursor.fetchall()
    return json.dumps(data, default=str)
