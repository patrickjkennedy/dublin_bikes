from flask import Flask, render_template, url_for, g, jsonify, request
from flask_app import application
import config
import pymysql.cursors
from conversion import changingTime
import pandas as pd
import simplejson as json
import datetime
import pickle
from os.path import join, dirname, realpath
import json as js

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

@application.route("/api/current_weather")
def get_weather():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM weather order by id desc limit 1")
        data = cursor.fetchall()
    return jsonify(data)

@application.route("/api/current_availability")
def get_current_availability():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM (SELECT * FROM dublin_bikes_availability limit 113) AS T ORDER BY number asc;")
        data = cursor.fetchall()
    return jsonify(data)

@application.route("/api/forecast")
def get_forecast():
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM forecast")
        data = cursor.fetchall()
    return jsonify(data)

@application.route("/user_input", methods=["GET", "POST"])
def user_input():

    #get form data user input
    fromStation =  request.args['StationselectFrom']
    toStation = request.args['StationselectTo']
    fromTime = changingTime(request.args['SelectcollectTime'])
    toTime = changingTime(request.args['SelectdropTime'])

    #change times to datetime strings
    fromTime = datetime.datetime.strptime(fromTime, '%Y-%m-%d %H:%M:%S')
    toTime = datetime.datetime.strptime(toTime, '%Y-%m-%d %H:%M:%S')

    #change weekday to string
    weekday = fromTime.strftime('%A')

    #change times to hours
    fromMins = fromTime.strftime('%M')
    toMins = toTime.strftime('%M')
    toTime = toTime.strftime('%H')
    fromTime = fromTime.strftime('%H')

    #save names for files
    pickle1 = weekday+'_'+ fromStation +'.pkl'
    pickle2 = weekday+'_'+ toStation +'.pkl'

    #get absolute paths for pickle files
    path1 = join(dirname(realpath(__file__)), 'static/pickles/'+pickle1)
    path2 = join(dirname(realpath(__file__)), 'static/pickles/'+pickle2)

    #load both pickle files
    with open(path1, 'rb') as handleFrom:
        model1 = pickle.load(handleFrom)
    with open(path2, 'rb') as handleTo:
        model2 = pickle.load(handleTo)

    X = initDF()
    Y = initDF()
    input1 = generateInput(fromTime)
    input2 = generateInput(toTime)

    setValuesDF(X, input1)
    setValuesDF(Y, input2)

    result1 = model1.predict(X)
    result2 = model2.predict(Y)

    return jsonify(from_station=fromStation, from_station_bike_availability=int(round(result1[0])), from_time=fromTime,
                    to_station=toStation, to_time=toTime, to_station_stand_availability=int(round(result2[0])), from_mins=fromMins,
                    to_mins=toMins)

def initDF():
    # Initialize the hours list
    hours = [0] * 24
    # Initialize weather continuous features
    weather_data = [0] * 4
    # Combine to form initial vector
    data = [hours + weather_data]

    df = pd.DataFrame(data, columns=['hour_0', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9',
                                  'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16', 'hour_17',
                                  'hour_18', 'hour_19', 'hour_20', 'hour_21', 'hour_22', 'hour_23', 'main_temp', 'main_pressure', 'main_humidity', 'wind_speed'])

    return df

def setValuesDF(df, dict):
    df['hour_' + dict['hour']][0] = 1
    df['main_temp'][0] = dict['main_temp']
    df['main_pressure'][0] = dict['main_pressure']
    df['main_humidity'][0] = dict['main_humidity']
    df['wind_speed'][0] = dict['wind_speed']

def generateInput(hour):
    if len(hour) == 2:
        hour = hour[1]
    paramDict = {}
    current_weather = get_weather().get_json()
    mainTemp = current_weather[0]['main_temp']
    mainPressure = current_weather[0]['main_pressure']
    mainHumidity =  current_weather[0]['main_humidity']
    windSpeed = current_weather[0]['wind_speed']
    paramDict['hour'] = hour
    paramDict['main_temp'] = mainTemp
    paramDict['main_pressure'] = mainPressure
    paramDict['main_humidity'] = mainHumidity
    paramDict['wind_speed'] = windSpeed
    return paramDict

@application.route("/api/station_occupancy_weekly/<int:station_id>")
def get_station_occupancy_weekly(station_id):
    connection = get_db()
    days = ["Mon", "Tue", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    df = pd.read_sql_query("SELECT * FROM dublin_bikes_availability WHERE number = %(number)s LIMIT 0, 18446744073709551615",
    connection, params={"number":station_id})
    df.set_index('last_update', inplace=True)
    df['weekday'] = df.index.weekday
    df['weekday'] = df.index.weekday
    mean_available_stands = df[['available_bike_stands','weekday']].groupby('weekday').mean().round(1)
    mean_available_bikes = df[['available_bikes', 'weekday']].groupby('weekday').mean().round(1)
    mean_available_stands.index = days
    mean_available_bikes.index = days
    return jsonify(mean_available_stands=mean_available_stands.to_json(), mean_available_bikes=mean_available_bikes.to_json())
