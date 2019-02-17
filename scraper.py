import requests
import mysql.connector
import time

# Setup the database connection
mydb = mysql.connector.connect(
  host="HOST-HERE",
  user="USER-HERE",
  passwd="PASSWORD-HERE",
  database="DB-HERE",
  auth_plugin='mysql_native_password'
)

# Get the data from the API
url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=API-KEY-HERE"
response = requests.get(url)
data = response.json()


# Create the insert statement for the new data
sql = "INSERT INTO table_name_here (number, name, address, latitude, longitude, banking, bonus, " \
      "bike_stands, available_bike_stands, available_bikes, status, last_update) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

mycursor = mydb.cursor()

# Iterate through the data response object and perform inserts
for elem in range(0, len(data)):
    val = (data[elem]["number"], data[elem]["name"], data[elem]["address"], data[elem]["position"]["lat"],
           data[elem]["position"]["lng"], data[elem]["banking"], data[elem]["bonus"], data[elem]["bike_stands"],
           data[elem]["available_bike_stands"], data[elem]["available_bikes"], data[elem]["status"],
           time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[elem]["last_update"]/1000)))
    mycursor.execute(sql, val)

mydb.commit()

# Close the connection
mydb.close()


