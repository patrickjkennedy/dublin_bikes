import requests
import mysql.connector
import time
import sys
import config

# Setup the database connection
try:
    mydb = mysql.connector.connect(
        host=config.rds_host,
        user=config.rds_user,
        passwd=config.rds_password,
        database=config.rds_production_database,
        auth_plugin='mysql_native_password'
    )
except mysql.connector.Error as err:
    print("Unable to connect to database: {}".format(err))
    sys.exit(1)

url_forecast = "https://api.openweathermap.org/data/2.5/forecast?id=7778677&appid=e6fe8274aa40ec3cfad673280273873a"

response_forecast = requests.get(url_forecast)
data_forecast = response_forecast.json()

sql_forecast = "INSERT INTO forecast (Date_time, Weather_ID, Weather_main, Weather_description, Main_temp, Clouds, Wind_speed) "\
                "VALUES (%s,%s,%s,%s,%s,%s,%s)"

mycursor = mydb.cursor()

sql_truncate = "TRUNCATE forecast"
mycursor.execute(sql_truncate)
mydb.commit()

for i in range(8):
    val3=(data_forecast['list'][i]['dt'],data_forecast['list'][i]['weather'][0]['id'],
    data_forecast['list'][i]['weather'][0]['main'],data_forecast['list'][i]['weather'][0]['description'],
    data_forecast['list'][i]['main']['temp'], data_forecast['list'][i]['clouds']['all'], data_forecast['list'][i]['wind']['speed'])

    print(val3)
    mycursor.execute(sql_forecast, val3)

mydb.commit()

