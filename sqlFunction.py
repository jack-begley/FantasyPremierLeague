import gameweekSummary
import playerData
import genericMethods
import detailedStats
import Teams
import mysql.connector
import sqlite3 
import pandas
import json
import requests

#jackbegley
#thenoise360

def connect(user, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password
    )
    
    print(f"Connected: {mydb.server_host}:{mydb.server_port}")

    return mydb

def checkDatabases(user, password):
    mydb = connect(user, password)

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
      print(x)

def create(user, password, databaseName):
    mydb = connect(user, password)

    mycursor = mydb.cursor()
    try:
        mycursor.execute(f"CREATE DATABASE {databaseName}")
        print(f"Database \"{databaseName}\" created.")

    except:
        print("ERROR: database already exists")

  
def createTable(user, password, tableName, database, columnSpec):
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database=database
    )

    mycursor = mydb.cursor()

    columnSpecFormatted = columnSpec.replace("'","").replace('"','')

    try:
        ready = str(f"CREATE TABLE {tableName} ({columnSpec})").replace("'","")
        mycursor.execute(ready)
        print(f"Table \"{tableName}\" created.")

    except:
        print("ERROR: table already exists")

def read(db, databaseName):
    print("")

def update(db, databaseName):
    print("")

def delete(user, password, databaseName):
    mydb = connect(user, password)

    mycursor = mydb.cursor()

    mycursor.execute(f"DROP DATABASE {databaseName}")

    print(f"Database \"{databaseName}\" deleted.")

conversions = {
    'int': 'INT',
    'bool': 'TINYINT',
    'str': 'VARCHAR(255)'
    'NoneType'
    }

#user = input("Username: ")
user = "jackbegley"
#password = input("Password: ")
password = "Athome19369*"
db = "GameweekSummary"

checkDatabases(user, password)

create(user, password, "GameweekSummary")

checkDatabases(user, password)

JSON = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
Data = JSON.json()

specification = dict()

# === TODO: Get working for all of bootstrap static ====================================================================================================

#for section in Data:
#    tableName = section
#    for element in Data[section]:
#        if isinstance(element, dict) == True:
#            for values in element:
#                # MAKE THIS PART WORK WITHOUT EXCEPTIONS
#                if isinstance(element[values], list) == False and isinstance(element[values], dict) == False:
#                    valueType = str(type(element[values])).replace("<class","").replace(">","").replace("'","").replace(" ","")
#                    valueTypeConversion = conversions[valueType]
#                    specification[values] = valueTypeConversion
#            convertedColumns = ','.join("'"+str(x).replace('/','_') + " " + str(specification[x]) + "'" for x in specification.keys())
#            createTable(user, password, tableName, 'gameweeksummary', convertedColumns)
#            break

# ========================================================================================================================================================

# ============= FOR TESTING, MAKE FORMAL ===================================
for element in Data['events']:
    columns = ','.join("'"+str(x).replace('/','_')+"'" for x in element.keys())
    # TODO: FOR NOW NEED TO REMOVE LIST OR DICT, AND CONVER BOOL to 1/0
    values = ','.join("'"+str(x).replace('/','_')+"'" for x in element.values())
    sql = "INSERT INTO %s (%s) VALUES (%s);" % ('events', columns, values)
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database='gameweeksummary'
    )

    mycursor = mydb.cursor()
    mycursor.execute(sql)

#=================================================================================

# REMOVE ===============================================
result = json.loads(Dumps["elements"])

df = pandas.DataFrame(result)

delete(user, password, "GameweekSummary")

checkDatabases(user, password)

print("")
# ===============================================


#Now we need to create a connection to our sql database. We will be using sqlite for that.

#import sqlite3conn = sqlite3.connect("data.db")c = conn.cursor()

#We can now convert our JSON data from dataframe to sqlite format such as db or sqlite.

#df.to_sql("tablename",conn)
#Note: The first argument is the table name you will be storing your data in.