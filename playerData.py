from pprint import pprint
import requests
import json
import argparse
import csv 
import zipfile
import pyodbc
import aiohttp
import asyncio
import unicodecsv
import urllib.request
import urllib.parse
import tkinter
import datetime
from tkinter import filedialog
from tkinter import Tk
import unidecode
import sys, traceback
import re
import io
import math
from scipy.stats.stats import pearsonr 
from scipy.stats import linregress
from gameweekSummary import *
from genericMethods import *

#Setting up url construction

def mergeURL(sub):
    return 'https://fantasy.premierleague.com/api/' + sub;
# Syntax e.g. = print(mergeURL(userSummary))

# URL set up and league codes
from datetime import date
today = date.today()

# All gameweek data for a player (by gameweek)
def allPlayerDataBySurname(playerSurname):
    playerID = matchUserInputToList(playerSurname,generatePlayerIDToNameMatching())
    currentGameWeek = math.floor((datetime.datetime.now() - datetime.datetime(2019, 8, 5)).days/7)
    elementsList = dict()
    tempList = list()
    allPlayerDataReadable = generateJSONDumpsReadable(mergeURL('element-summary/')+str(playerID)+'/')
    PlayerList = dict()

    for data in allPlayerDataReadable['history']:        
        dumpsData = json.dumps(data)
        formattedData = json.loads(dumpsData)
        gameweek = formattedData['round']
        id = formattedData['element']
        for record in formattedData:
            elementName = record
        # Create data list for current player assigning to each key
        for record in formattedData:
            currentRound = formattedData['round']
            PlayerList[record] = formattedData[record]
        for element in PlayerList:
            if element not in elementsList:
                elementsList[element] = (PlayerList[element])
            else:
                elementsList[element] = str(elementsList[element]) + ',' + str(PlayerList[element])
        PlayerList = dict()

    return elementsList

# All gameweek data for a player (by gameweek)
def playerInfoByGameweek(gameweekNumber):
    None

# Create player first & last name list (and associated dictionary)
def generatePlayersFullNameList():
    # Initialise the arrays outside the loop so that they cannot be overriden
    gameweekSummaryListFull = list()
    gameweekSummarySub = "bootstrap-static/"
    url = mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = generateJSONDumpsReadable(url)

    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            firstName = formattedY['first_name']
            secondName = formattedY['second_name']
            fullName = f'{firstName} {secondName}'
            gameweekSummaryListFull.append(fullName)
    return generatePlayersFullNameList

# Create player id list
def generatePlayersIdsList():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDList = list()
    gameweekSummarySub = "bootstrap-static/"
    url = mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = generateJSONDumpsReadable(url)

    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            id = formattedY['id']
            playerIDList.append(id)
    
    return playerIDList

# Create player id list (and associated surname)
def generatePlayerIDToNameMatching():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDMatchList = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = generateJSONDumpsReadable(url)

    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            secondName = formattedY['second_name']
            cleanedSecondName = str.lower(unicodeReplace(secondName))
            id = formattedY['id']
            playerIDMatchList[cleanedSecondName] = id

    return playerIDMatchList

# Match User input to an array and return the result
def matchUserInputToList(userInput, listToMatchInputTo):
    result = listToMatchInputTo[userInput]
    return result

# Create player first & last name list (and associated dictionary)
def gatherHistoricalPlayerData():
    playerIDs = generatePlayerIDs()
    # create url's for the current player and extract data from the "History" file where the game week is the current game week
    currentGameWeek = math.floor((datetime.datetime.now() - datetime.datetime(2019, 8, 5)).days/7)
    length = len(playerIDs) - 1
    elementsList = dict()
    tempList = list()
    # Gather the player data
    for playerID in playerIDs:
        currentIndex = list(playerIDs).index(playerID)
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"Gather data for regression: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"Data for regression gathered: 100%")
            sys.stdout.flush()
            print("")

        allPlayerDataReadable = generateJSONDumpsReadable(mergeURL('element-summary/')+str(playerID)+'/')

        currentPlayerList = dict()

        for data in allPlayerDataReadable['history']:        
            dumpsData = json.dumps(data)
            formattedData = json.loads(dumpsData)
            gameweek = formattedData['round']
            id = formattedData['element']
            for record in formattedData:
                elementName = record
            # Create data list for current player assigning to each key
            for record in formattedData:
                currentRound = formattedData['round']
                currentPlayerList[record] = formattedData[record]
            for element in currentPlayerList:
                if element not in elementsList:
                    elementsList[element] = (currentPlayerList[element])
                else:
                    elementsList[element] = str(elementsList[element]) + ',' + str(currentPlayerList[element])
            currentPlayerList = dict()

    return elementsList

# Converts a dictionary that is string based to an integer list
def convertStringDictToInt(inputList, outputListName):
   # Get All data into integers in a comma seperated list
    outputListName = dict()
    currentList = dict()
    tempList = list()
    for element in inputList:
        try:
            outputListName[element] = list(map(float, inputList[element].split(',')))
        except BaseException:
            if element != "kickoff_time":
                currentList[element] = list(map(str, inputList[element].split(',')))
                for n in currentList[element]:
                    if n != 'None':
                        n = int((n).replace('False', '0').replace('True', '1'))
                        tempList.append(n)
                    else:
                        None
                outputListName[element] = tempList
            else:
                None
    return outputListName

# Generate coefficients between an array of data and one key in that array
def correlcoeffGeneration(nameOfArrayToCorrelate, keyToCorrelateAgainstName):
    # Correlation time
    correlations = dict()
    currentX = dict()
    currentY = dict()
    currentCorrel = list()
    for element in nameOfArrayToCorrelate:
        length = len(nameOfArrayToCorrelate) - 1
        currentIndex = list(nameOfArrayToCorrelate).index(element)
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"Running regression: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"Regression complete: 100%")
            sys.stdout.flush()
            print("")
        if element != 'kickoff_time':
            currentX = nameOfArrayToCorrelate[element]
            currentY = nameOfArrayToCorrelate[keyToCorrelateAgainstName]
            currentCorrel = linregress(currentX,currentY)
            correlations[element] = currentCorrel
        else:
            None

# Export the player data by gameweek where the playerID's have been gathered
def exportPlayerDataByGameweek(playerIDs):
    playerName = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = generateJSONDumpsReadable(url)

    for playerID in playerIDs:
        currentPlayerURL = mergeURL('element-summary/')+str(playerID)+'/'
        allPlayerDataReadable = generateJSONDumpsReadable(currentPlayerURL)
        
        currentPlayerList = dict()
        
        currentIndex = list(playerIDs).index(playerID)
        length = len(playerIDs) - 1
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"Gathering data by player: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"Data by player name gathered: 100%")
            sys.stdout.flush()
            print("")
        for element in gameweekSummaryDataReadable['elements']:
            if playerID == element['id']:
                firstName = element['first_name']
                secondName = element['second_name']
                fullName = f'{firstName} {secondName}'
                currentPlayerURL = mergeURL('element-summary/')+str(playerID)+'/'
                allPlayerDataReadable = generateJSONDumpsReadable(currentPlayerURL)
                currentPlayerList = dict()                
                gameweekDict = dict()
                for data in allPlayerDataReadable['history']:        
                    dumpsData = json.dumps(data)
                    formattedData = json.loads(dumpsData)
                    currentDict = dict()
                    gameweek = formattedData['round']
                    for element in formattedData:
                        currentDict[element] = formattedData[element]
                    gameweekDict[gameweek] = currentDict
                playerName[fullName] = gameweekDict
                break


     # Open a window allowing the user to specify the file save path using a File Explorer
    root = tkinter.Tk()
    savePath =tkinter.filedialog.askdirectory()
    root.destroy()
    # Get the file path
    fileName = input("What do you want to call the file? > ")
    filePath = f"{savePath}/{today} - {fileName}.csv"
    # Create the dictionaries for the data that we are going to print into csv
    playerExportList = dict()
    headerList = list()
    headerList.append('Full_name')
    headerList.append('gameweek')
    printed = 0

    # Open the csv with our file name and path so we can write in the data
    with open(filePath, 'w', newline='', encoding='utf-8') as out:
        # Create the csv writers with the settings we want (e.g. the different delimiters)
        csv_out_tab_seperator = csv.writer(out, delimiter="\t")
        csv_out_comma_seperator = csv.writer(out, delimiter=",")

        for player in playerName:
            length = len(playerName)-1
            playerDumps = json.dumps(playerName)
            formattedPlayer = json.loads(playerDumps)
            currentIndex = list(playerName).index(player)
            playerClean = player.strip().replace("'","`")
            runPercentageComplete = str(round((currentIndex/length)*100,1))
            if runPercentageComplete != "100.0":
                sys.stdout.write('\r'f"Compiling exportable data file: {runPercentageComplete}%"),
                sys.stdout.flush()
            else:
                sys.stdout.write('\r'"")
                sys.stdout.write(f"Exportable data file ready for use: {runPercentageComplete}%")
                sys.stdout.flush()
                print("")
                print("")

            for gameweek in playerName[player]:
                gameweekData = playerName[player][gameweek]
                gameweekDumps = json.dumps(gameweekData)
                formattedGameweek = json.loads(gameweekDumps)
                for data in formattedGameweek:
                    if data not in headerList:
                        headerList.append(data)
                    else:
                        if printed != 1:
                            csv_out_comma_seperator.writerow(headerList)
                            printed = 1

            for gameweek in playerName[player]:
                gameweekData = playerName[player][gameweek]
                gameweekDumps = json.dumps(gameweekData)
                formattedGameweek = json.loads(gameweekDumps)
                currentList = list()
                currentList.append(gameweek)
                for data in formattedGameweek:
                    currentAddition = str(formattedGameweek[data]).strip()
                    currentList.append(currentAddition)
                playerExportList[player] = currentList
                playerExportListAsString = str(playerExportList[player]).replace("'","")
                exportablePlayerData = playerExportListAsString.replace('[','').replace(']','').replace('"',"")
                csv_out_tab_seperator.writerow([f'{playerClean},{exportablePlayerData}'])
    print("Done")