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
def correlcoeffGeneration():

    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDs = list()
    
    gameweekSummarySub = "bootstrap-static/"

    url = mergeURL(gameweekSummarySub)
    gameweekSummaryJSON = requests.get(url)
    gameweekSummaryData = gameweekSummaryJSON.json()
    gameweekSummaryDataDumps = json.dumps(gameweekSummaryData)
    gameweekSummaryDataReadable = json.loads(gameweekSummaryDataDumps)
    
    # Get all of the player id's
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            currentPlayerID = formattedY['id']
            playerIDs.append(currentPlayerID)
    playerIDs.sort()
    
    # create url's for the current player and extract data from the "History" file where the game week is the current game week
    startOfTournament = datetime.datetime(2019, 8, 5)
    currentDate = datetime.datetime.now()
    dateDelta = currentDate - startOfTournament
    daysSinceTournamentStarted = dateDelta.days
    currentGameWeek = math.floor(daysSinceTournamentStarted/7)

    historyByWeek = dict()
    
    for playerID in playerIDs:
        currentPlayerURL = mergeURL('element-summary/')+str(playerID)+'/'
        
        allPlayerJSON = requests.get(currentPlayerURL)
        allPlayerData = allPlayerJSON.json()
        allPlayerDumps = json.dumps(allPlayerData)
        allPlayerDataReadable = json.loads(allPlayerDumps)

        elementsList = dict()
        currentPlayerList = dict()

        for data in allPlayerDataReadable['history']:        
            dumpsData = json.dumps(data)
            formattedData = json.loads(dumpsData)
            gameweek = formattedData['round']
            id = formattedData['element']
            # Add all keys to dictionary
            for record in formattedData:
                elementName = record
            # Create data list for current player assigning to each key
            for record in formattedData:
                round = formattedData['round']
                currentPlayerList[record] = formattedData[record]
            for element in currentPlayerList:
                if element not in elementsList:
                    elementsList[element] = (currentPlayerList[element])
                else:
                    elementsList[element].append(currentPlayerList[element])
            currentPlayerList = dict()
    historyByWeek.append(currentPlayerList) 


#coreApi = 'https://fantasy.premierleague.com/api/'
#playerSummary = "element-summary/"

#playersJSON = requests.get(mergeURL(playerSummary))
#playersData = playersJSON.json()
#playersDataDumps = json.dumps(playersData)
#playersDataReadable = json.loads(playersDataDumps)