import requests
import mysql.connector
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

# Get the data from the API
url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + config.jcdecaux_api_key
try:
    response = requests.get(url)
    data = response.json()
except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

# Create the insert statement for the new data
sql = "INSERT INTO dublin_bikes_static (number, contract_name, name, address, latitude, longitude, banking, " \
      "bonus) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

try:
    mycursor = mydb.cursor()

    # Iterate through the data response object and perform inserts
    for elem in range(0, len(data)):
        val = (data[elem]["number"], data[elem]["contract_name"], data[elem]["name"], data[elem]["address"],
               data[elem]["position"]["lat"], data[elem]["position"]["lng"], data[elem]["banking"], data[elem]["bonus"])
        mycursor.execute(sql, val)

    mydb.commit()

    # Close the connection
    mydb.close()

except mysql.connector.Error as err:
    print("Unable to connect to database: {}".format(err))
    sys.exit(1)
