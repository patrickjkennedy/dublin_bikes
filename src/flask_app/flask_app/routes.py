from flask import Flask, render_template, url_for, g, jsonify, request
from flask_app import application
import config
import pymysql.cursors
from conversion import changingTime
import pandas as pd
import simplejson as json

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

@application.teardown_appcontext
def close_connection(exception):
    try:
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
    except pymysql.Error as error:
        print("While closing with database :", error)
        raise

@application.route('/')
@application.route('/index')
def index():
    data_stations = get_stations().get_json()
    data_current_availability = get_current_availability().get_json()
    return render_template('index.html', title='Home', data_stations=data_stations, data_current_availability=data_current_availability, map_key=config.map_url)

@application.route("/api/stations")
def get_stations():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dublin_bikes_static")
        data = cursor.fetchall()
    return jsonify(data)

@application.route("/api/current_availability")
def get_current_availability():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM scraper.dublin_bikes_availability order by id desc limit 113;")
        data = cursor.fetchall()
    return jsonify(data)

@application.route("/api/forecast")
def get_forecast():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM scraper.forecast")
        data = cursor.fetchall()
    return jsonify(data)

@application.route("/user_input", methods=["GET", "POST"])
def user_input():
    fromStation =  request.form.get('StationselectFrom')
    toStation = request.form.get('StationselectTo')
    fromTime = changingTime(request.form.get('SelectcollectTime'))
    toTime = changingTime(request.form.get('SelectdropTime'))
    result =  json.dumps({'From Station': fromStation, 'To Station': toStation, 'From Time': fromTime, 'To Time':toTime})
    return(result)

@application.route("/api/station_occupancy_weekly/<int:station_id>")
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
