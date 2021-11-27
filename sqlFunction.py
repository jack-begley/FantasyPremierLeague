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
import os
import sys
from datetime import datetime
import pytz

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


conversions = {
    'int': 'INT',
    'bool': 'INT',
    'str': 'TEXT',
    'float': 'FLOAT'
    }

#user = input("Username: ")
user = "jackbegley"
#password = input("Password: ")
password = "Athome19369*"

#jackbegley
#thenoise360

# [ ] Events = https://fantasy.premierleague.com/api/event/{currentGameweek}/live
# [Y] Bootstrap = https://fantasy.premierleague.com/api/bootstrap-static/
# [Y] Element Summary = https://fantasy.premierleague.com/api/element-summary/{n}/
# [ ] MyTeam = https://fantasy.premierleague.com/api/my-team/{teamID}
# [ ] Other teams = https://fantasy.premierleague.com/api/entry/{teamID}/event/{gameweekNumber}/picks/
# [ ] Fixtures = https://fantasy.premierleague.com/api/fixtures/?event={gwNow}


# TODO: DELETE ONCE CURRENT IMPORT ERROR IS SORTED (SEE LINE 1)
def generateCurrentGameweek():
    JSON = requests.get("https://fantasy.premierleague.com/api/entry/1/")
    bootstrapStaticData = JSON.json()
    DumpsPre = json.dumps(bootstrapStaticData)
    dumps = json.loads(DumpsPre)
    for keys in dumps:
        if keys == 'current_event':
            return dumps[keys]

# Run percentage
def runPercentage(maxLen, currentIndex, messageToDisplay, completeMessage):
    runPercentageComplete = str(round((currentIndex/maxLen)*100,1))
    if runPercentageComplete != "100.0":
        sys.stdout.write('\r'f"{messageToDisplay}: {runPercentageComplete}%                      "),
        sys.stdout.flush()
    else:
        sys.stdout.write('\r'"")
        sys.stdout.write(f"{completeMessage}: {runPercentageComplete}%                           ")
        sys.stdout.flush()
        print("")

def reformattedSortedTupleAsDict(listOfTuples):
    reformattedDict = list()
    for tuples in listOfTuples:
        item0 = tuples[0]
        reformattedDict.append(item0)

    return reformattedDict

def unicodeReplace(string):
    cleanedString = string.replace("Á", "A").replace("á", "a").replace("À", "A").replace("à", "a").replace("Ȧ", "A").replace("ȧ", "a").replace("Â", "A").replace("â", "a").replace("Ä", "A").replace("ä", "a").replace("Ǎ", "A").replace("ǎ", "a").replace("Ă", "A").replace("ă", "a").replace("Ā", "A").replace("ā", "a").replace("Ã", "A").replace("ã", "a").replace("Å", "A").replace("å", "a").replace("Ą", "A").replace("ą", "a").replace("Ⱥ", "A").replace("Ǡ", "A").replace("ǡ", "a").replace("Ǻ", "A").replace("ǻ", "a").replace("Ǟ", "A").replace("ǟ", "a").replace("Ȁ", "A").replace("ȁ", "a").replace("Ȃ", "A").replace("ȃ", "a").replace("Æ", "AE").replace("æ", "ae").replace("Ǽ", "AE").replace("ǽ", "ae").replace("Ǣ", "AE").replace("ǣ", "ae").replace("Ḃ", "B").replace("ḃ", "b").replace("ƀ", "b").replace("Ƀ", "B").replace("Ɓ", "B").replace("Ƃ", "B").replace("ƃ", "b").replace("Ƅ", "b").replace("ƅ", "b").replace("Ć", "C").replace("ć", "c").replace("Ċ", "C").replace("ċ", "c").replace("Ĉ", "C").replace("ĉ", "c").replace("Č", "C").replace("č", "c").replace("Ç", "C").replace("ç", "c").replace("Ȼ", "C").replace("ȼ", "c").replace("Ƈ", "C").replace("ƈ", "c").replace("Ɔ", "C").replace("Ḋ", "D").replace("ḋ", "d").replace("Ď", "D").replace("ď", "d").replace("Đ", "D").replace("đ", "d").replace("Ƌ", "D").replace("ƌ", "d").replace("Ɗ", "D").replace("Ð", "D").replace("ð", "d").replace("ƍ", "d").replace("ȸ", "db").replace("Ǳ", "DZ").replace("ǲ", "Dz").replace("ǳ", "dz").replace("Ǆ", "DZ").replace("ǅ", "Dz").replace("ǆ", "dz").replace("Ɖ", "D").replace("ȡ", "d").replace("É", "E").replace("é", "e").replace("È", "E").replace("è", "e").replace("Ė", "E").replace("ė", "e").replace("Ê", "E").replace("ê", "e").replace("Ë", "E").replace("ë", "e").replace("Ě", "E").replace("ě", "e").replace("Ĕ", "E").replace("ĕ", "e").replace("Ē", "E").replace("ē", "e").replace("Ę", "E").replace("ę", "e").replace("Ȩ", "E").replace("ȩ", "e").replace("Ɇ", "E").replace("ɇ", "e").replace("Ȅ", "E").replace("ȅ", "e").replace("Ȇ", "E").replace("ȇ", "e").replace("Ǝ", "E").replace("ǝ", "e").replace("Ə", "e").replace("Ɛ", "e").replace("Ȝ", "e").replace("ȝ", "e").replace("Ḟ", "F").replace("ḟ", "f").replace("Ƒ", "F").replace("ƒ", "f").replace("Ǵ", "G").replace("ǵ", "g").replace("Ġ", "G").replace("ġ", "g").replace("Ĝ", "G").replace("ĝ", "g").replace("Ǧ", "G").replace("ǧ", "g").replace("Ğ", "G").replace("ğ", "g").replace("Ģ", "G").replace("ģ", "g").replace("Ǥ", "G").replace("ǥ", "g").replace("Ɠ", "G").replace("Ɣ", "g").replace("Ĥ", "H").replace("ĥ", "h").replace("Ȟ", "H").replace("ȟ", "h").replace("Ħ", "H").replace("ħ", "h").replace("ƕ", "h").replace("Ƕ", "H").replace("ı", "i").replace("Í", "I").replace("í", "i").replace("Ì", "I").replace("ì", "i").replace("İ", "I").replace("Î", "i").replace("î", "I").replace("Ï", "i").replace("ï", "I").replace("Ǐ", "i").replace("ǐ", "I").replace("Ĭ", "i").replace("ĭ", "I").replace("Ī", "i").replace("ī", "I").replace("Ĩ", "i").replace("ĩ", "I").replace("Į", "i").replace("į", "I").replace("Ɨ", "i").replace("Ȉ", "I").replace("ȉ", "i").replace("Ȋ", "I").replace("ȋ", "i").replace("Ɩ", "I").replace("Ĳ", "IJ").replace("ĳ", "ij").replace("ȷ", "j").replace("Ĵ", "J").replace("ĵ", "j").replace("ǰ", "j").replace("Ɉ", "j").replace("ɉ", "j").replace("ĸ", "k").replace("Ǩ", "K").replace("ǩ", "k").replace("Ķ", "K").replace("ķ", "k").replace("Ƙ", "K").replace("ƙ", "k").replace("Ĺ", "L").replace("ĺ", "l").replace("Ŀ", "L").replace("ŀ", "l").replace("Ľ", "L").replace("ľ", "l").replace("Ļ", "L").replace("ļ", "l").replace("ƚ", "l").replace("Ƚ", "L").replace("Ł", "L").replace("ł", "l").replace("ƛ", "L").replace("Ǉ", "LJ").replace("ǈ", "Lj").replace("ǉ", "lj").replace("ȴ", "l").replace("Ṁ", "M").replace("ṁ", "m").replace("Ɯ", "M").replace("Ń", "N").replace("ń", "n").replace("Ǹ", "N").replace("ǹ", "n").replace("Ň", "N").replace("ň", "n").replace("Ñ", "N").replace("ñ", "n").replace("Ņ", "N").replace("ņ", "n").replace("Ɲ", "N").replace("ŉ", "n").replace("ƞ", "n").replace("Ƞ", "N").replace("Ǌ", "NJ").replace("ǋ", "Nj").replace("ǌ", "nj").replace("ȵ", "n").replace("Ŋ", "N").replace("ŋ", "n").replace("Ó", "O").replace("ó", "o").replace("Ò", "O").replace("ò", "o").replace("Ȯ", "O").replace("ȯ", "o").replace("Ô", "O").replace("ô", "o").replace("Ö", "O").replace("ö", "o").replace("Ǒ", "O").replace("ǒ", "o").replace("Ŏ", "O").replace("ŏ", "o").replace("Ō", "O").replace("ō", "o").replace("Õ", "O").replace("õ", "o").replace("Ǫ", "O").replace("ǫ", "o").replace("Ő", "O").replace("ő", "o").replace("Ɵ", "O").replace("Ø", "O").replace("ø", "o").replace("Ȱ", "O").replace("ȱ", "o").replace("Ȫ", "O").replace("ȫ", "o").replace("Ǿ", "O").replace("ǿ", "o").replace("Ȭ", "O").replace("ȭ", "o").replace("Ǭ", "O").replace("ǭ", "o").replace("Ȍ", "O").replace("ȍ", "o").replace("Ȏ", "O").replace("ȏ", "o").replace("Ơ", "O").replace("ơ", "o").replace("Ƣ", "O").replace("ƣ", "o").replace("Œ", "OE").replace("œ", "oe").replace("Ȣ", "O").replace("ȣ", "o").replace("Ṗ", "P").replace("ṗ", "p").replace("Ƥ", "P").replace("ƥ", "p").replace("Ɋ", "P").replace("ɋ", "p").replace("ȹ", "qp").replace("Ʀ", "R").replace("Ŕ", "R").replace("ŕ", "r").replace("Ř", "R").replace("ř", "r").replace("Ŗ", "R").replace("ŗ", "r").replace("Ɍ", "R").replace("ɍ", "r").replace("Ȑ", "R").replace("ȑ", "r").replace("Ȓ", "R").replace("ȓ", "r").replace("Ś", "S").replace("ś", "s").replace("Ṡ", "S").replace("ṡ", "s").replace("Ŝ", "S").replace("ŝ", "s").replace("Š", "S").replace("š", "s").replace("Ş", "S").replace("ş", "s").replace("Ș", "S").replace("ș", "s").replace("ȿ", "s").replace("Ʃ", "S").replace("Ƨ", "S").replace("ƨ", "s").replace("ƪ", "S").replace("ß", "ss").replace("ſ", "t").replace("ẛ", "t").replace("Ṫ", "T").replace("ṫ", "t").replace("Ť", "T").replace("ť", "t").replace("Ţ", "T").replace("ţ", "t").replace("Ƭ", "T").replace("ƭ", "t").replace("ƫ", "t").replace("Ʈ", "T").replace("Ț", "T").replace("ț", "t").replace("Ⱦ", "T").replace("ȶ", "t").replace("Þ", "t").replace("þ", "t").replace("Ŧ", "T").replace("ŧ", "t").replace("Ú", "U").replace("ú", "u").replace("Ù", "U").replace("ù", "u").replace("Û", "U").replace("û", "u").replace("Ü", "U").replace("ü", "u").replace("Ǔ", "U").replace("ǔ", "u").replace("Ŭ", "U").replace("ŭ", "u").replace("Ū", "U").replace("ū", "u").replace("Ũ", "U").replace("ũ", "u").replace("Ů", "U").replace("ů", "u").replace("Ų", "U").replace("ų", "u").replace("Ű", "U").replace("ű", "u").replace("Ʉ", "U").replace("Ǘ", "U").replace("ǘ", "u").replace("Ǜ", "U").replace("ǜ", "u").replace("Ǚ", "U").replace("ǚ", "u").replace("Ǖ", "U").replace("ǖ", "u").replace("Ȕ", "U").replace("ȕ", "u").replace("Ȗ", "U").replace("ȗ", "u").replace("Ư", "U").replace("ư", "u").replace("Ʊ", "U").replace("Ʋ", "U").replace("Ʌ", "V").replace("Ẃ", "W").replace("ẃ", "w").replace("Ẁ", "W").replace("ẁ", "w").replace("Ŵ", "W").replace("ŵ", "w").replace("Ẅ", "W").replace("ẅ", "w").replace("ƿ", "x").replace("Ƿ", "X").replace("Ý", "Y").replace("ý", "y").replace("Ỳ", "Y").replace("ỳ", "y").replace("Ŷ", "Y").replace("ŷ", "y").replace("ÿ", "Y").replace("Ÿ", "y").replace("Ȳ", "Y").replace("ȳ", "y").replace("Ɏ", "Y").replace("ɏ", "y").replace("Ƴ", "Y").replace("ƴ", "y").replace("Ź", "Z").replace("ź", "z").replace("Ż", "Z").replace("ż", "z").replace("Ž", "Z").replace("ž", "z").replace("Ƶ", "Z").replace("ƶ", "z").replace("Ȥ", "Z").replace("ȥ", "z").replace("ɀ", "Z").replace("Ʒ", "z").replace("Ǯ", "Z").replace("ǯ", "z").replace("Ƹ", "Z").replace("ƹ", "z").replace("ƺ", "Z").replace("ƾ", "z").replace("Ɂ", "Z").replace("ɂ", "z")
    return cleanedString


# =================================================

def getDataFromDatabaseAsDict(user, password, db, sql):
    dbConnect = connectToDB(user, password, db)
    cursor = dbConnect.cursor(dictionary=True)
    cursor.execute(sql)
    data = list()
    for row in cursor:
        data.append(row)
    return data


def dataConvertion(value):
    try:
        convert = float(value)
        return convert
    except:
        try:
            convert = int(value)
            return convert
        except:
            convert = str(value)
            return convert


def connectToSQL(user, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password
    )
    
    return mydb

def connectToDB(user, password, database):
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database=database
    )
    
    return mydb

def checkDatabases(user, password):
    mydb = connectToSQL(user, password)

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
      print(x)

def createDatabase(user, password, databaseName):
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
    mydb = connectToDB(user, password, databaseName)

    mycursor = mydb.cursor()

    mycursor.execute(f"DROP DATABASE {databaseName}")

    print(f"Database \"{databaseName}\" deleted.")

def typeConverter(value):
    if isinstance(value, str):
        try:
            return float(value)
        except:
            if isinstance(value, bool):
                return bool(value)
            else:
                return str(value)
    if isinstance(value, int):
        return int(value)



def createAllSuitableTables(user, password, database, table, datafeed):
    specification = dict()
    JSON = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    bootstrapStaticData = JSON.json()
    if table == 'history_past':
        specification['id'] = 'INT'
    for element in datafeed[table]:
        if isinstance(element, dict) == True:
            for item in element:
                if isinstance(element[item], dict) == False and isinstance(element[item], list) == False:
                    valueFormatted = typeConverter(element[item])
                    valueType = str(type(valueFormatted)).replace("<class","").replace(">","").replace("'","").replace(" ","")
                    if item == "news_added" or item == "news":
                        valueTypeConversion = "TEXT"
                    elif valueType == "NoneType":
                        valueTypeConversion = "INT"
                    else:
                        valueTypeConversion = conversions[valueType]
                    specification[item] = valueTypeConversion
                if isinstance(element[item], dict) == True or isinstance(element[item], list) == True:
                    for data in element[item]:
                        if isinstance(data, dict) == True or isinstance(data, list) == True:
                            for datapoint in data:
                                valueFormatted = typeConverter(data[datapoint])
                                valueType = str(type(valueFormatted)).replace("<class","").replace(">","").replace("'","").replace(" ","")
                                if valueType == "NoneType":
                                    valueTypeConversion = "INT"
                                else:
                                    valueTypeConversion = conversions[valueType]
                                dataList = list(data.values())
                                specification[f"{item}_{dataList[0]}"] = valueTypeConversion
                        else:
                            valueFormatted = typeConverter(data)
                            valueType = str(type(valueFormatted)).replace("<class","").replace(">","").replace("'","").replace(" ","")
                            if valueType == "NoneType":
                                valueTypeConversion = "INT"
                            else:
                                valueTypeConversion = conversions[valueType]
                            specification[data] = valueTypeConversion
        else:
            valueFormatted = typeConverter(element)
            valueType = str(type(datafeed[table][element])).replace("<class","").replace(">","").replace("'","").replace(" ","")
            if valueType == "NoneType":
                valueTypeConversion = "INT"
            elif isinstance(datafeed[table][element], dict) == True or isinstance(datafeed[table][element], list) == True:
                    for data in datafeed[table][element]:
                        valueType = str(type(data)).replace("<class","").replace(">","").replace("'","").replace(" ","")
                        if valueType == "NoneType":
                            valueTypeConversion = "INT"
                        else:
                            valueTypeConversion = conversions[valueType]
                            specification[f"{element}_{data}"] = valueTypeConversion
            else:
                valueTypeConversion = conversions[valueType]
            specification[element] = valueTypeConversion

    convertedColumns = ','.join("'"+str(x).replace('/','_').replace("-","_").replace("+","") + " " + str(specification[x]) + "'" for x in specification.keys())
    createTable(user, password, table, database, convertedColumns)

# === TODO: Condense to a single method ====================================================================================================
def updateEventsTable(user, password, database):
    table = 'events'
    JSON = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    bootstrapStaticData = JSON.json()
    deleteTable(user, password, table, database)
    createAllSuitableTables(user, password, database, table, bootstrapStaticData)
    currentGameweek = generateCurrentGameweek()
    for element in bootstrapStaticData[table]:
        elementsKept = dict()
        for item in element:
            if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = 0
                elif valueType == "bool":
                    if element[item] == True:
                        value = 1
                    if element[item] == False:
                        value = 0
                else:
                    value = element[item]
                elementsKept[item] = value

            if isinstance(element[item], dict) == True or isinstance(element[item], list) == True:
                for data in element[item]:
                    if isinstance(data, dict) == True or isinstance(data, list) == True:
                        for datapoint in data:
                            valueType = str(type(data[datapoint])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                            if valueType == "NoneType":
                                value = 0
                            elif valueType == "bool":
                                if data[datapoint] == True:
                                    value = 1
                                if data[datapoint] == False:
                                    value = 0
                            else:
                                value = data[datapoint]
                            dataList = list(data.values())
                            elementsKept[f"{item}_{dataList[0]}"] = value
                    else:
                        valueType = str(type(element[item][data])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                        if valueType == "NoneType":
                            value = 0
                        elif valueType == "bool":
                            if data == True:
                                value = 1
                            if data == False:
                                value = 0
                        else:
                            value = element[item][data]
                        elementsKept[data] = value

        columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
        values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())
        sql = "INSERT INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

        if int(element['name'].replace("Gameweek ","")) < (currentGameweek + 1):
            dbConnect = connectToDB(user, password, database)
            cursor = dbConnect.cursor()
            cursor.execute(sql)
            dbConnect.commit()
            print(cursor.rowcount, f"Record inserted successfully into {table} table")
            cursor.close()

        else:
            break

def updateElementsTable(user, password, database):
    table = 'elements'
    deleteTable(user, password, table, database)
    createAllSuitableTables(user, password, database, table, bootstrapStaticData)
    currentGameweek = generateCurrentGameweek()

    dbConnect = connectToDB(user, password, database)
    cursor = dbConnect.cursor()

    for element in bootstrapStaticData[table]:
        elementsKept = dict()
        for item in element:
            if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = 0
                elif valueType == "bool":
                    if element[item] == True:
                        value = 1
                    if element[item] == False:
                        value = 0
                else:
                    value = element[item]
                    if isinstance(value, str) == True:
                        valueClean = str(unicodeReplace(str(value))).replace("'","")
                        value = valueClean
                elementsKept[item] = value

        columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
        values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())
        sql = "INSERT INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

        cursor.execute(sql)
        dbConnect.commit()
        print(cursor.rowcount, f"Record inserted successfully into {table} table")

    cursor.close()

def updateGameSettingsTable(user, password, database):
    table = 'game_settings'
    deleteTable(user, password, table, database)
    createAllSuitableTables(user, password, database, table, bootstrapStaticData)
    currentGameweek = generateCurrentGameweek()
    elementsKept = dict()
    for element in bootstrapStaticData[table]:
        if isinstance(bootstrapStaticData[table][element], list) == False and isinstance(bootstrapStaticData[table][element], dict) == False:
            valueType = str(type( bootstrapStaticData[table][element])).replace("<class","").replace(">","").replace("'","").replace(" ","")
            if valueType == "NoneType":
                value = 0
            elif valueType == "bool":
                if  bootstrapStaticData[table][element] == True:
                    value = 1
                if  bootstrapStaticData[table][element] == False:
                    value = 0
            else:
                value = bootstrapStaticData[table][element]
                if isinstance(value, str) == True:
                    valueClean = str(unicodeReplace(str(value))).replace("'","")
                    value = valueClean
            elementsKept[element] = value

        if isinstance(bootstrapStaticData[table][element], list) == True or isinstance(bootstrapStaticData[table][element], dict) == True:
            for data in bootstrapStaticData[table][element]:
                valueType = str(type(data)).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = 0
                elif valueType == "bool":
                    if  data == True:
                        value = 1
                    if  data == False:
                        value = 0
                else:
                    value =  data
                    if isinstance(value, str) == True:
                        valueClean = str(unicodeReplace(str(value))).replace("'","")
                        value = valueClean
                dataCleaned = str(data).replace('/','_').replace("-","_").replace("+","")
                elementsKept[f"{element}_{dataCleaned}"] = value

    columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
    values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())
    sql = "INSERT INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

    dbConnect = connectToDB(user, password, database)
    cursor = dbConnect.cursor()
    cursor.execute(sql)
    dbConnect.commit()
    print(cursor.rowcount, f"Record inserted successfully into {table} table")
    cursor.close()

def updateElementStatsTable(user, password, database):
    table = 'element_stats'
    deleteTable(user, password, table, database)
    createAllSuitableTables(user, password, database, table, bootstrapStaticData)
    currentGameweek = generateCurrentGameweek()

    dbConnect = connectToDB(user, password, database)
    cursor = dbConnect.cursor()

    for element in bootstrapStaticData[table]:
        elementsKept = dict()
        for item in element:
            if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = 0
                elif valueType == "bool":
                    if element[item] == True:
                        value = 1
                    if element[item] == False:
                        value = 0
                else:
                    value = element[item]
                    if isinstance(value, str) == True:
                        valueClean = str(unicodeReplace(str(value))).replace("'","")
                        value = valueClean
                elementsKept[item] = value

        columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
        values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())
        sql = "INSERT INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

        cursor.execute(sql)
        dbConnect.commit()
        print(cursor.rowcount, f"Record inserted successfully into {table} table")

    cursor.close()

def updatePhasesTable(user, password, database):
    table = 'phases'
    deleteTable(user, password, table, database)
    createAllSuitableTables(user, password, database, table, bootstrapStaticData)
    currentGameweek = generateCurrentGameweek()

    dbConnect = connectToDB(user, password, database)
    cursor = dbConnect.cursor()
    
    for element in bootstrapStaticData[table]:
        elementsKept = dict()
        for item in element:
            if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = 0
                elif valueType == "bool":
                    if element[item] == True:
                        value = 1
                    if element[item] == False:
                        value = 0
                else:
                    value = element[item]
                    if isinstance(value, str) == True:
                        valueClean = str(unicodeReplace(str(value))).replace("'","")
                        value = valueClean
                elementsKept[item] = value

        columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
        values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())
        sql = "INSERT INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

        cursor.execute(sql)
        dbConnect.commit()
        print(cursor.rowcount, f"Record inserted successfully into {table} table")
    cursor.close()

def updateTeamsTable(user, password, database):
    table = 'teams'
    deleteTable(user, password, table, database)
    createAllSuitableTables(user, password, database, table, bootstrapStaticData)
    currentGameweek = generateCurrentGameweek()

    dbConnect = connectToDB(user, password, database)
    cursor = dbConnect.cursor()

    for element in bootstrapStaticData[table]:
        elementsKept = dict()
        for item in element:
            if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = 0
                elif valueType == "bool":
                    if element[item] == True:
                        value = 1
                    if element[item] == False:
                        value = 0
                else:
                    value = element[item]
                    if isinstance(value, str) == True:
                        valueClean = str(unicodeReplace(str(value))).replace("'","")
                        value = valueClean
                elementsKept[item] = value

        columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
        values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())
        sql = "INSERT INTO `%s` (%s) VALUES (%s);" % (table, columns, values)
        cursor.execute(sql)
        dbConnect.commit()
        print(cursor.rowcount, f"Record inserted successfully into {table} table")
    cursor.close()

# =====================================================================================================================================================

# Events table =====================================================================================================

def updateEventsDatabase(user, password, database):
    table = 'elements'
    currentGameweek = generateCurrentGameweek()
    n = 1
    headerData = requests.get("https://fantasy.premierleague.com/api/event/1/live").json()
    formattedPlayerData = dict()
    formattedEvents = dict()
    for player in headerData["elements"]:
        for record in player:
            if record not in list(formattedEvents.keys()):
                if isinstance(player[record], dict) == False and isinstance(player[record], list) == False:
                    formattedPlayerData[record] = player[record]
                if isinstance(player[record], dict) == True:
                    for item in player[record]:
                        formattedPlayerData[item] = player[record][item]
                if record == "explain":
                    for item in player['explain'][0]:
                        if isinstance(player['explain'][0][item], dict) == False and  isinstance(player['explain'][0][item], list) == False:
                            formattedPlayerData[item] = headerData['elements'][0]['explain'][0][item]
                        if isinstance(player['explain'][0][item], list) == True:
                            for values in player['explain'][0][item]:
                                for value in values:
                                    if value != "identifier":
                                        name = f"{values['identifier']}_{value}"
                                        formattedPlayerData[name] = values[value]

    prepared = dict()
    prepared['elements'] = formattedPlayerData
    deleteTable(user, password, table, database)
    createAllSuitableTables(user, password, database, table, prepared)

    x = 1

    while n <= currentGameweek:
        JSON = requests.get(f"https://fantasy.premierleague.com/api/event/{n}/live")
        eventsData = JSON.json()
        currentGameweek = generateCurrentGameweek()

        dbConnect = connectToDB(user, password, database)
        cursor = dbConnect.cursor()

        formattedEvents = dict()
        for player in eventsData["elements"]:
            formattedPlayerData = dict()
            for record in player:
                if isinstance(player[record], dict) == False and isinstance(player[record], list) == False:
                    formattedPlayerData[record] = player[record]
                if isinstance(player[record], dict) == True:
                    for item in player[record]:
                        formattedPlayerData[item] = player[record][item]
                if record == "explain":
                    for item in player['explain'][0]:
                        if isinstance(player['explain'][0][item], dict) == False and  isinstance(player['explain'][0][item], list) == False:
                            formattedPlayerData[item] = headerData['elements'][0]['explain'][0][item]
                        if isinstance(player['explain'][0][item], list) == True:
                            for values in player['explain'][0][item]:
                                for value in values:
                                    if value != "identifier":
                                        name = f"{values['identifier']}_{value}"
                                        formattedPlayerData[name] = values[value]
            formattedEvents[x] = formattedPlayerData
            x += 1

        for element in formattedEvents:
            elementsKept = dict()
            for item in formattedEvents[element]:
                if isinstance(formattedEvents[element][item], list) == False and isinstance(formattedEvents[element][item], dict) == False:
                    valueType = str(type(formattedEvents[element][item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                    if valueType == "NoneType":
                        value = 0
                    elif valueType == "bool":
                        if formattedEvents[element][item] == True:
                            value = 1
                        if formattedEvents[element][item] == False:
                            value = 0
                    else:
                        value = formattedEvents[element][item]
                        if isinstance(value, str) == True:
                            valueClean = str(unicodeReplace(str(value))).replace("'","")
                            value = valueClean
                    elementsKept[item] = value

            columns = ','.join("`"+str(x).replace('/','_')+"`" for x in prepared['elements'])
            finalEventData = dict()
            for i in prepared['elements']:
                if i in elementsKept.keys():
                    finalEventData[i] = elementsKept[i]
                else:
                    finalEventData[i] = 0
            values = ','.join("'"+str(x).replace('/','_')+"'" for x in finalEventData.values())
            sql = "INSERT INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

            cursor.execute(sql)
            dbConnect.commit()

        print(f"Running week {n} of {currentGameweek}")

        n += 1

# ===================================================================================================================

# === TODO: Condense to a single method ====================================================================================================

def updateFixturesTable(user, password, database, datafeed):
    table = 'fixtures'
    currentGameweek = generateCurrentGameweek()
    # TODO - create a create table method, maybe under a "start of season update" thing, then update this method to run without dropping the table
    currentDateTime = datetime.now(pytz.utc)
    # 2021-11-27T12:30:00Z
    
    dbConnect = connectToDB(user, password, database)
    cursor = dbConnect.cursor()

    for element in currentElement[table]:
        fixtureTime = datetime.strptime(element['kickoff_time'], "%Y-%m-%dT%H:%M:%S%z")
        if currentDateTime < fixtureTime:
            elementsKept = dict()
            id = element['id']
            sqlCompare = f"SELECT id from {table} where id = {id}"

            mydb = mysql.connector.connect(
              host="localhost",
              user=user,
              password=password,
              database=database
            )

            mycursor = mydb.cursor()
            mycursor.execute(sqlCompare)
            myresult = mycursor.fetchall()

            if not myresult:
                for item in element:
                    if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                        valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                        if valueType == "NoneType":
                            value = 0
                        elif valueType == "bool":
                            if element[item] == True:
                                value = 1
                            if element[item] == False:
                                value = 0
                        else:
                            value = element[item]
                            if isinstance(value, str) == True:
                                valueClean = str(unicodeReplace(str(value))).replace("'","")
                                value = valueClean
                        elementsKept[item] = value

                columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
                values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())

                sql = "INSERT IGNORE INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

                cursor.execute(sql)
                dbConnect.commit()
                print(cursor.rowcount, f"Record inserted successfully into {table} table")

    cursor.close()

def updateHistoryTable(user, password, database, datafeed):
    table = 'history'
    currentGameweek = generateCurrentGameweek()

    dbConnect = connectToDB(user, password, database)
    cursor = dbConnect.cursor()

    for element in currentElement[table]:
        elementsKept = dict()
        for item in element:
            if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = 0
                elif valueType == "bool":
                    if element[item] == True:
                        value = 1
                    if element[item] == False:
                        value = 0
                else:
                    value = element[item]
                    if isinstance(value, str) == True:
                        valueClean = str(unicodeReplace(str(value))).replace("'","")
                        value = valueClean
                elementsKept[item] = value

        columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
        values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())

        sql = "INSERT IGNORE INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

        cursor.execute(sql)
        dbConnect.commit()
        print(cursor.rowcount, f"Record inserted successfully into {table} table")

    cursor.close()

def updateHistoryPastTable(user, password, database, datafeed, playerId):
    table = 'history_past'
    currentGameweek = generateCurrentGameweek()

    dbConnect = connectToDB(user, password, database)
    cursor = dbConnect.cursor()

    for element in currentElement[table]:
        elementsKept = dict()
        elementsKept['id'] = n
        for item in element:
            if isinstance(element[item], list) == False and isinstance(element[item], dict) == False:
                valueType = str(type(element[item])).replace("<class","").replace(">","").replace("'","").replace(" ","")
                if valueType == "NoneType":
                    value = 0
                elif valueType == "bool":
                    if element[item] == True:
                        value = 1
                    if element[item] == False:
                        value = 0
                else:
                    value = element[item]
                    if isinstance(value, str) == True:
                        valueClean = str(unicodeReplace(str(value))).replace("'","")
                        value = valueClean
                elementsKept[item] = value

        columns = ','.join("`"+str(x).replace('/','_')+"`" for x in elementsKept.keys())
        values = ','.join("'"+str(x).replace('/','_')+"'" for x in elementsKept.values())

        sql = "INSERT IGNORE INTO `%s` (%s) VALUES (%s);" % (table, columns, values)

        cursor.execute(sql)
        dbConnect.commit()
        print(cursor.rowcount, f"Record inserted successfully into {table} table")

    cursor.close()

# TEST - TOP 10 transfers out ====================== TODO: REMOVE ===============
data = getDataFromDatabaseAsDict(user, password, "2021_2022_BootstrapStatic", "SELECT id, transfers_out_event FROM `2021_2022_bootstrapstatic`.`elements` ORDER BY transfers_out_event desc LIMIT 10;")

print("")
# REMOVE TO HERE =================================================================

# BOOTSTRAP STATIC =================================================================
bootstrapTrue = input("Do you want to update 2021_2022_BootstrapStatic (Y/N)> ")
if bootstrapTrue == "Y" or bootstrapTrue == "y":
    db = "2021_2022_BootstrapStatic"
    updateEventsTable(user, password, db)
    updateElementsTable(user, password, db)
    updateElementStatsTable(user, password, db)
    updateGameSettingsTable(user, password, db)
    updatePhasesTable(user, password, db)
    updateTeamsTable(user, password, db)

#= ELEMENT SUMMARU ================================================================================

elementSummaryTrue = input("Do you want to update 2021_2022_ElementSummary (Y/N)> ")
if elementSummaryTrue == "Y" or elementSummaryTrue == "y":
    db = "2021_2022_ElementSummary"

    mydb = mysql.connector.connect(
      host="localhost",
      user=user,
      password=password,
      database="2021_2022_bootstrapstatic"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT id FROM elements")

    myresult = mycursor.fetchall()

    ids = reformattedSortedTupleAsDict(myresult)
    minimum = min(ids)
    maximum = max(ids)

    n = minimum

    updateHistoryPast = input("Do you want to update 'history_past' (Only needs updated once a season) (Y/N)> ")
    
    JSON = requests.get(f"https://fantasy.premierleague.com/api/element-summary/1/")
    currentElement = JSON.json()
    for element in currentElement:
        if updateHistoryPast == "y" or updateHistoryPast == 'Y' or element != "history_past":
            deleteTable(user, password, element, db)
        createAllSuitableTables(user, password, db, element, currentElement)


    # while n <= maximum:
    while n <= maximum:
        JSON = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{n}/")
        currentElement = JSON.json()
        runPercentage(maximum, n, f"Running player {n} of {maximum}", "All databases updated                         ")
        updateFixturesTable(user, password, db, currentElement)
        updateHistoryTable(user, password, db, currentElement)
        if updateHistoryPast == "y" or updateHistoryPast == 'Y':
            updateHistoryPastTable(user, password, db, currentElement, n)
        n += 1

    print("")

# DETAILED STATS ==============================================================================================================
# https://stackoverflow.com/questions/9336270/using-a-python-dict-for-a-sql-insert-statement

detailedStatsTrue = input("Do you want to update 2021_2022_DetailedStats (Y/N)> ")
if detailedStatsTrue == "Y" or detailedStatsTrue == "y":
    db = "2021_2022_DetailedStats"
    playerList = detailedStats.getAllPlayers()
    players = detailedStats.getPlayerStats(playerList)
    players = detailedStats.getPlayerStatsDetailed(playerList)

# EVENTS ==============================================================================================================

eventsTrue = input("Do you want to update 2021_2022_Events (Y/N)> ")
if eventsTrue == "Y" or eventsTrue == "y":
    db = "2021_2022_Events"
    updateEventsDatabase(user, password, db)