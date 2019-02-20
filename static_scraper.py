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
url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={API-KEY}"
response = requests.get(url)
data = response.json()


# Create the insert statement for the new data
sql = "INSERT INTO dublin_bikes_static (number, contract_name, name, address, latitude, longitude, banking, " \
      "bonus) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

mycursor = mydb.cursor()

# Iterate through the data response object and perform inserts
for elem in range(0, len(data)):
    val = (data[elem]["number"], data[elem]["contract_name"], data[elem]["name"], data[elem]["address"],
           data[elem]["position"]["lat"], data[elem]["position"]["lng"], data[elem]["banking"], data[elem]["bonus"])
    mycursor.execute(sql, val)

mydb.commit()

# Close the connection
mydb.close()
