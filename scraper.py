import requests
import mysql.connector
import time

# Setup the database connection
mydb = mysql.connector.connect(
    host="host-name",
    user="user-name",
    passwd="insert-password",
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
sql_bikes = "INSERT INTO dublin_bikes (number, name, address, latitude, longitude, banking, bonus, " \
      "bike_stands, available_bike_stands, available_bikes, status, last_update) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

sql_weather = "INSERT INTO Weather (main, icon, temp_min, temp_max, wind)" \
                "VALUES (%s, %s, %s, %s, %s)"

mycursor = mydb.cursor()

# Iterate through the data response object and perform inserts
for elem in range(0, len(data_bikes)):
    val = (data_bikes[elem]["number"], data_bikes[elem]["name"], data_bikes[elem]["address"], data_bikes[elem]["position"]["lat"],
           data_bikes[elem]["position"]["lng"], data_bikes[elem]["banking"], data_bikes[elem]["bonus"], data_bikes[elem]["bike_stands"],
           data_bikes[elem]["available_bike_stands"], data_bikes[elem]["available_bikes"], data_bikes[elem]["status"],
           time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_bikes[elem]["last_update"]/1000)))
    mycursor.execute(sql_bikes, val)

val2=(data_weather['weather'][0]['main'], data_weather['weather'][0]['icon'],data_weather['main']['temp_min'], data_weather['main']['temp_max'],data_weather['wind']['speed'])

mycursor.execute(sql_weather, val2)
    
mydb.commit()

# Close the connection
mydb.close()
