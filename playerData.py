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
from tkinter import filedialog
from tkinter import Tk
import sys, traceback
import re
import io


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
    
    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            currentPlayerID = formattedY['id']
            playerIDs.append(currentPlayerID)
    

#coreApi = 'https://fantasy.premierleague.com/api/'
#playerSummary = "element-summary/"

#playersJSON = requests.get(mergeURL(playerSummary))
#playersData = playersJSON.json()
#playersDataDumps = json.dumps(playersData)
#playersDataReadable = json.loads(playersDataDumps)