import requests
import mysql.connector
import time

# Setup the database connection
mydb = mysql.connector.connect(
    host="host-name",
    user="user-name",
    passwd="password",
    database="database-name",
    auth_plugin='mysql_native_password'

)

# Get the data from the API
url_bikes = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={API-KEY}"
url_weather = 'https://api.openweathermap.org/data/2.5/weather?id=7778677&appid={API-KEY}'


response_bikes = requests.get(url_bikes)
data_bikes = response_bikes.json()

response_weather = requests.get(url_weather)
data_weather = response_weather.json()


# Create the insert statement for the new data
sql_bikes = "INSERT INTO dublin_bikes_availability (number, bike_stands, available_bike_stands, " \
            "available_bikes, status, last_update) " \
            "VALUES (%s, %s, %s, %s, %s, %s)"

sql_weather = "INSERT INTO weather (coord_lon, coord_lat, weather_id, weather_main, weather_description, "\
            "weather_icon, base, main_temp, main_pressure, main_humidity, main_temp_min, main_temp_max, "\
            "visibility, wind_speed, wind_deg, clouds_all, dt, sys_type, sys_id, sys_message, sys_country, "\
            "sys_sunrise, sys_sunset, city_id, city_name, cod) "\
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

mycursor = mydb.cursor()

# Iterate through the data response object and perform inserts
for elem in range(0, len(data_bikes)):
    val = (data[elem]["number"], data[elem]["bike_stands"], data[elem]["available_bike_stands"],
           data[elem]["available_bikes"], data[elem]["status"],
           time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[elem]["last_update"]/1000)))

    mycursor.execute(sql_bikes, val)

val2=(data_weather['coord']['lon'],data_weather['coord']['lat'],data_weather['weather'][0]['id'],data_weather['weather'][0]['main'],
      data_weather['weather'][0]['description'],data_weather['weather'][0]['icon'],data_weather['base'],data_weather['main']['temp'],
      data_weather['main']['pressure'],data_weather['main']['humidity'],data_weather['main']['temp_min'],data_weather['main']['temp_max'],
      data_weather['visibility'],data_weather['wind']['speed'],data_weather['wind']['deg'],data_weather['clouds']['all'],
      time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_weather['dt'])),data_weather['sys']['type'],
      data_weather['sys']['id'],data_weather['sys']['message'],data_weather['sys']['country'],
      time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_weather['sys']['sunrise'])),
      time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_weather['sys']['sunset'])),data_weather['id'],data_weather['name'],data_weather['cod'])

mycursor.execute(sql_weather, val2)

mydb.commit()

# Close the connection
mydb.close()
