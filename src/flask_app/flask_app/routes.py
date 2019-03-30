from flask import Flask, render_template, url_for, g, jsonify
from flask_app import app
import os
import config
import simplejson as json
import pymysql.cursors
import pandas as pd

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

@app.route("/api/station_occupancy_weekly/<int:station_id>")
def get_station_occupancy_weekly(station_id):
    connection = get_db()
    days = ["Mon", "Tue", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    df = pd.read_sql_query("SELECT * FROM scraper.dublin_bikes_availability WHERE number = %(number)s LIMIT 0, 18446744073709551615",
    connection, params={"number":station_id})
    df.set_index('last_update', inplace=True)
    df['weekday'] = df.index.weekday
    df['weekday'] = df.index.weekday
    mean_available_stands = df[['available_bike_stands','weekday']].groupby('weekday').mean().round(1)
    mean_available_bikes = df[['available_bikes', 'weekday']].groupby('weekday').mean().round(1)
    mean_available_stands.index = days
    mean_available_bikes.index = days
    return jsonify(mean_available_stands=mean_available_stands.to_json(), mean_available_bikes=mean_available_bikes.to_json())
