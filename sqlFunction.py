# TODO: -- FIX CYCLICAL IMPORT ERRORS
import gameweekSummary
import playerData
import genericMethods
import detailedStats
import Teams
# -------------------------------
import mysql.connector
import sqlite3 
import pandas
import json
import requests

#jackbegley
#thenoise360

# TODO: DELETE ONCE CURRENT IMPORT ERROR IS SORTED (SEE LINE 1)
def generateCurrentGameweek():
    JSON = requests.get("https://fantasy.premierleague.com/api/entry/1/")
    Data = JSON.json()
    DumpsPre = json.dumps(Data)
    dumps = json.loads(DumpsPre)
    for keys in dumps:
        if keys == 'current_event':
            return dumps[keys]
# =================================================


def connectToSQL(user, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password
    )
    
    print(f"Connected: {mydb.server_host}:{mydb.server_port}")

    return mydb

def connectToDB(user, password, database):
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database=database
    )
    
    print(f"Connected: {mydb.server_host}:{mydb.server_port}")

    return mydb

def checkDatabases(user, password):
    mydb = connectToSQL(user, password)

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
      print(x)

def create(user, password, databaseName):
    mydb = connectToSQL(user, password)

    mycursor = mydb.cursor()
    try:
        mycursor.execute(f"CREATE DATABASE {databaseName}")
        print(f"Database \"{databaseName}\" created.")

    except:
        print("ERROR: database already exists")

  
def createTable(user, password, tableName, database, columnSpec):
    mydb = connectToDB(user, password, database)

    mycursor = mydb.cursor()

    columnSpecFormatted = columnSpec.replace("'","").replace('"','')

    try:
        ready = str(f"CREATE TABLE {tableName} ({columnSpec})").replace("'","")
        mycursor.execute(ready)
        print(f"Table \"{tableName}\" created.")

    except:
        print("ERROR: table already exists")

    mycursor.execute("SHOW TABLES")

    for x in mycursor:
      print(x)

def deleteTable(user, password, tableName, database):
    mydb = connectToDB(user, password, database)
    
    mycursor = mydb.cursor()

    try:
        ready = str(f"DROP TABLE {tableName}")
        mycursor.execute(ready)
        print(f"Table \"{tableName}\" deleted.")

    except:
        print("ERROR: table doesn't exists")

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
    'str': 'VARCHAR(255)',
    }

#user = input("Username: ")
user = "jackbegley"
#password = input("Password: ")
password = "Athome19369*"
db = "GameweekSummary"

checkDatabases(user, password)

JSON = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
Data = JSON.json()

specification = dict()

# === TODO: Get working for all of bootstrap static ====================================================================================================
def createAllSuitableTables(user, password):
    for section in Data:
        tableName = section
        if isinstance(Data[section], dict) == True or isinstance(Data[section], list) == True:
            for element in Data[section]:
                if isinstance(element, dict) == True:
                    for item in element:
                        if isinstance(item, dict) == False:
                            # MAKE THIS PART WORK WITHOUT EXCEPTIONS
                            valueType = str(type(item)).replace("<class","").replace(">","").replace("'","").replace(" ","")
                            if valueType == "NoneType":
                                valueTypeConversion = "CHAR"
                            else:
                                valueTypeConversion = conversions[valueType]
                            specification[item] = valueTypeConversion
                else:
                    # MAKE THIS PART WORK WITHOUT EXCEPTIONS
                    valueType = str(type(element)).replace("<class","").replace(">","").replace("'","").replace(" ","")
                    if valueType == "NoneType":
                        valueTypeConversion = "CHAR"
                    else:
                        valueTypeConversion = conversions[valueType]
                    specification[element] = valueTypeConversion
            convertedColumns = ','.join("'"+str(x).replace('/','_') + " " + str(specification[x]) + "'" for x in specification.keys())
            createTable(user, password, tableName, 'gameweeksummary', convertedColumns)


# ========================================================================================================================================================

# ============= FOR TESTING, MAKE FORMAL ===================================
def updateEventsTable(user, password, database):
    deleteTable(user, password, 'events', database)
    createAllSuitableTables(user, password)
    currentGameweek = generateCurrentGameweek()
    for element in Data['events']:
        elementsKept = dict()
        for item in element:
            if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = "-"
                elif valueType == "bool":
                    if element[item] == True:
                        value = 1
                    if element[item] == False:
                        value = 0
                else:
                    value = element[item]
                elementsKept[item] = value
        # TODO: Only drop and create a table for Events
        columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
        values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())
        sql = "INSERT INTO `%s` (%s) VALUES (%s);" % ('events', columns, values)

        if int(element['name'].replace("Gameweek ","")) < (currentGameweek + 1):
            dbConnect = connectToDB(user, password, database)
            cursor = dbConnect.cursor()
            cursor.execute(sql)
            dbConnect.commit()
            print(cursor.rowcount, "Record inserted successfully into events table")
            cursor.close()

        else:
            break

updateEventsTable(user, password, db)
#=================================================================================
