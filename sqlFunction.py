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

#If using pyodbc
#https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15

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

    mycursor.execute(f"CREATE DATABASE {databaseName}")

    print(f"Database \"{databaseName}\" created.")

def read(db, databaseName):
    print("")

def update(db, databaseName):
    print("")

def delete(user, password, databaseName):
    mydb = connect(user, password)

    mycursor = mydb.cursor()

    mycursor.execute(f"DROP DATABASE {databaseName}")

    print(f"Database \"{databaseName}\" deleted.")



#user = input("Username: ")
user = "jackbegley"
#password = input("Password: ")
password = "Athome19369*"
db = "GameweekSummary"

checkDatabases(user, password)

#create(user, password, "GameweekSummary")

checkDatabases(user, password)

JSON = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
Data = JSON.json()
Dumps = json.dumps(Data)
result = json.loads(Dumps["elements"])

df = pandas.DataFrame(result)

delete(user, password, "GameweekSummary")

checkDatabases(user, password)

print("")


#Now we need to create a connection to our sql database. We will be using sqlite for that.

#import sqlite3conn = sqlite3.connect("data.db")c = conn.cursor()

#We can now convert our JSON data from dataframe to sqlite format such as db or sqlite.

#df.to_sql("tablename",conn)
#Note: The first argument is the table name you will be storing your data in.