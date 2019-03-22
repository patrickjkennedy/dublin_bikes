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
            db=config.rds_production_database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    # Make this exception actually work
    except pymysql.Error as error:
        print("While connecting with database :", error)
        raise

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    try:
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
    except pymysql.Error as error:
        print("While closing with database :", error)
        raise

@app.route('/')
@app.route('/index')
def index():
    result_stations = get_stations()
    result_current_availability = get_current_availability()
    data_stations = json.loads(result_stations)
    data_current_availability = json.loads(result_current_availability)
    return render_template('index.html', title='Home', data_stations=data_stations, data_current_availability=data_current_availability, map_key=config.map_url)

@app.route("/api/stations")
def get_stations():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dublin_bikes_static")
        data = cursor.fetchall()
    return json.dumps(data, default=str)

@app.route("/api/current_availability")
def get_current_availability():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM scraper.dublin_bikes_availability order by id desc limit 113;")
        data = cursor.fetchall()
    return json.dumps(data, default=str)
