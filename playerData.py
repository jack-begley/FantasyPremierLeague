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
import sys, traceback
import re
import io
import math
from scipy.stats.stats import pearsonr 
from scipy.stats import linregress

#Setting up url construction

def mergeURL(sub):
    return 'https://fantasy.premierleague.com/api/' + sub;
# Syntax e.g. = print(mergeURL(userSummary))

# URL set up and league codes
from datetime import date
today = date.today()

# All gameweek data for a player (by gameweek)
def allPlayerDataBySurname(playerSurnasme):
    none

# All gameweek data for a player (by gameweek)
def playerInfoByGameweek(gameweekNumber):
    none

# All gameweek data for all players printed into .csv
def allPlayersAllGameweeksToExcel():
    none

# Create player first & last name list (and associated dictionary)
def gatherHistoricalPlayerData():

    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDs = list()
    
    gameweekSummarySub = "bootstrap-static/"

    url = mergeURL(gameweekSummarySub)
    gameweekSummaryJSON = requests.get(url)
    gameweekSummaryData = gameweekSummaryJSON.json()
    gameweekSummaryDataDumps = json.dumps(gameweekSummaryData)
    gameweekSummaryDataReadable = json.loads(gameweekSummaryDataDumps)
    
    # Get all of the player id's
    for ids in gameweekSummaryDataReadable['elements']:
        dumpsIds = json.dumps(ids)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(ids,dict):
            formattedIds = json.loads(dumpsIds)
            currentPlayerID = formattedIds['id']
            playerIDs.append(currentPlayerID)
    playerIDs.sort()
    # create url's for the current player and extract data from the "History" file where the game week is the current game week
    startOfTournament = datetime.datetime(2019, 8, 5)
    currentDate = datetime.datetime.now()
    dateDelta = currentDate - startOfTournament
    daysSinceTournamentStarted = dateDelta.days
    currentGameWeek = math.floor(daysSinceTournamentStarted/7)
    length = len(playerIDs) - 1
    elementsList = dict()
    allData = dict()
    currentList = dict()
    tempList = list()
    # Gather the player data
    for playerID in playerIDs:
        currentIndex = list(playerIDs).index(playerID)
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"(1/4) Gather data for regression: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"(1/4) Data for regression gathered: 100%")
            sys.stdout.flush()
            print("")

        currentPlayerURL = mergeURL('element-summary/')+str(playerID)+'/'
        
        allPlayerJSON = requests.get(currentPlayerURL)
        allPlayerData = allPlayerJSON.json()
        allPlayerDumps = json.dumps(allPlayerData)
        allPlayerDataReadable = json.loads(allPlayerDumps)
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
    # Get All data into integers in a comma seperated list
    for element in elementsList:
        try:
            allData[element] = list(map(float, elementsList[element].split(',')))
        except BaseException:
            if element != "kickoff_time":
                currentList[element] = list(map(str, elementsList[element].split(',')))
                for n in currentList[element]:
                    if n != 'None':
                        n = int((n).replace('False', '0').replace('True', '1'))
                        tempList.append(n)
                    else:
                        None
                allData[element] = tempList
            else:
                None
    correlcoeffGeneration(elementsList)

def correlcoeffGeneration(elementsList):
    # Correlation time
    correlations = dict()
    currentX = dict()
    currentY = dict()
    currentCorrel = list()
    for element in elementsList:
        length = len(elementsList) - 1
        currentIndex = list(elementsList).index(element)
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"(2/4) Running regression: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"(2/4) Regression complete: 100%")
            sys.stdout.flush()
            print("")
        if element != 'kickoff_time':
            currentX = allData[element]
            currentY = allData['total_points']
            currentCorrel = linregress(currentX,currentY)
            correlations[element] = currentCorrel
        else:
            None

    exportPlayerDataByGameweek(allPlayerDataReadable, playerIDs)

def exportPlayerDataByGameweek(allPlayerDataReadable, playerIDs):
    playerName = dict()
    
    gameweekSummarySub = "bootstrap-static/"

    url = mergeURL(gameweekSummarySub)
    gameweekSummaryJSON = requests.get(url)
    gameweekSummaryData = gameweekSummaryJSON.json()
    gameweekSummaryDataDumps = json.dumps(gameweekSummaryData)
    gameweekSummaryDataReadable = json.loads(gameweekSummaryDataDumps)
    for playerID in playerIDs:
        currentIndex = list(playerIDs).index(playerID)
        length = len(playerIDs) - 1
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"(3/4) Gathering data by player: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"(3/4) Data by player name gathered: 100%")
            sys.stdout.flush()
            print("")
        for element in gameweekSummaryDataReadable['elements']:
            if playerID == element['id']:
                firstName = element['first_name']
                secondName = element['second_name']
                fullName = f'{firstName} {secondName}'
                currentPlayerURL = mergeURL('element-summary/')+str(playerID)+'/'
        
                allPlayerJSON = requests.get(currentPlayerURL)
                allPlayerData = allPlayerJSON.json()
                allPlayerDumps = json.dumps(allPlayerData)
                allPlayerDataReadable = json.loads(allPlayerDumps)
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
                sys.stdout.write('\r'f"(4/4) Compiling exportable data file: {runPercentageComplete}%"),
                sys.stdout.flush()
            else:
                sys.stdout.write('\r'"")
                sys.stdout.write(f"(4/4) Exportable data file ready for use: {runPercentageComplete}%")
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