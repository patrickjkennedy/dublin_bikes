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

try:
    # Get the data from the API
    url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + config.jcdecaux_api_key
    response = requests.get(url)
    data = response.json()
except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

try:
    # Create the insert statement for the new data
    sql_insert = "INSERT INTO dublin_bikes_static (number, contract_name, name, address, latitude, longitude, banking, " \
                 "bonus) " \
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # Create a cursor
    mycursor = mydb.cursor()

    # Remove foreign key check
    sql_fk_check = "SET FOREIGN_KEY_CHECKS=0"
    mycursor.execute(sql_fk_check)
    mydb.commit()

    # Truncate existing values
    sql_truncate = "TRUNCATE dublin_bikes_static"
    mycursor.execute(sql_truncate)
    mydb.commit()

    # Readd foreign key check
    sql_fk_check = "SET FOREIGN_KEY_CHECKS=1"
    mycursor.execute(sql_fk_check)
    mydb.commit()

    # Iterate through the data response object and perform inserts
    for elem in range(0, len(data)):
        val = (data[elem]["number"], data[elem]["contract_name"], data[elem]["name"], data[elem]["address"],
               data[elem]["position"]["lat"], data[elem]["position"]["lng"], data[elem]["banking"], data[elem]["bonus"])
        mycursor.execute(sql_insert, val)
    mydb.commit()

    # Close the connection
    mydb.close()

except mysql.connector.Error as err:
    print("Unable to connect to database: {}".format(err))
    sys.exit(1)
