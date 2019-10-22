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
from genericMethods import *

# URL set up and league codes
from datetime import date
today = date.today()

# Export current data set into excel
def exportToExcelPlayers():
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

    gameweekSummarySub = "bootstrap-static/"

    url = mergeURL(gameweekSummarySub)
    gameweekSummaryJSON = requests.get(url)
    gameweekSummaryData = gameweekSummaryJSON.json()
    gameweekSummaryDataDumps = json.dumps(gameweekSummaryData)
    gameweekSummaryDataReadable = json.loads(gameweekSummaryDataDumps)

    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        formattedY = json.loads(dumpsY)
        currentList = list()
        firstName = formattedY['first_name']
        secondName = formattedY['second_name']
        fullName = f'{firstName} {secondName}'
        for data in formattedY:
            # Add to the current list, which is then added to the dictionary by each player - this is how we overcome garbage collection
            currentAddition = str(formattedY[data]).strip()
            currentList.append(currentAddition)
            if data not in headerList:
                headerList.append(data)
        playerExportList[fullName] = currentList

    # Open the csv with our file name and path so we can write in the data
    with open(filePath, 'w', newline='', encoding='utf-8') as out:
        # Create the csv writers with the settings we want (e.g. the different delimiters)
        csv_out_tab_seperator = csv.writer(out, delimiter="\t")
        csv_out_comma_seperator = csv.writer(out, delimiter=",")
        csv_out_comma_seperator.writerow(headerList)

        # For each player in our dictionary, run the command which writes in a row of data
        for player in playerExportList:
            playerClean = player.strip().replace("'","`")
            length = len(playerExportList)-1
            playerDumps = json.dumps(playerExportList)
            formattedPlayer = json.loads(playerDumps)
            currentIndex = list(playerExportList).index(player)
            playerExportListAsString = str(playerExportList[player]).replace("'","")
            exportablePlayerData = playerExportListAsString.replace('[','').replace(']','').replace('"',"")
            # write out all of the data with the tab delimiter seperating each item of the list
            csv_out_tab_seperator.writerow([f'{playerClean},{exportablePlayerData}'])

            # Percentage complete measured by the length of the dictionary and where the current index is in relation to the total number
            runPercentageComplete = str(round((currentIndex/length)*100,1))
            if runPercentageComplete != "100.0":
                sys.stdout.write('\r'f"Creating .csv file: {runPercentageComplete}%"),
                sys.stdout.flush()
            else:
                sys.stdout.write('\r'"")
                sys.stdout.write(f"Export Successful!: {runPercentageComplete}%")
                sys.stdout.flush()
                print("")
                print("")
    
# Print all of the player data in the console
def printAllData(urlAddOn, fileName):

    url = mergeURL(urlAddOn)

    # In order to either read in the index of the item, or the item name we either need the loaded version, or the dumped version respectively
    fileNameJSON = requests.get(url)
    fileNameData = fileNameJSON.json()
    fileNameDataDumps = json.dumps(fileNameData)
    fileNameDataReadable = json.loads(fileNameDataDumps)

    for x in fileNameDataReadable:
        dumpsX = json.dumps(x)
        readableX = json.loads(dumpsX)
        test = fileNameDataReadable[x]
        if isinstance(test, int) == False:
            print(x + ":")
            for y in fileNameDataReadable[x]:
                dumpsY = json.dumps(y)
                if isinstance(y,dict):
                    formattedY = json.loads(dumpsY)
                    for z in formattedY:
                        print("%s: %s" % (z, formattedY[z]))
                else:
                    print("%s: %s" % (y, fileNameDataReadable[x][y]))
        else:
             print("%s: %s" % (x, fileNameDataReadable[x]))

        print("")

    endRoutine()

# Getting the information of a player based on their surname
def playerInfoBySurname(playerSurname):

    gameweekSummarySub = "bootstrap-static/"

    # In order to either read in the index of the item, or the item name we either need the loaded version, or the dumped version respectively
    url = mergeURL(gameweekSummarySub)
    gameweekSummaryJSON = requests.get(url)
    gameweekSummaryData = gameweekSummaryJSON.json()
    gameweekSummaryDataDumps = json.dumps(gameweekSummaryData)
    gameweekSummaryDataReadable = json.loads(gameweekSummaryDataDumps)

    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        playerInApi = False
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            secondName = formattedY['second_name']

            #Generate a list for the headers
            if str.lower(formattedY["second_name"]) == playerSurname:
                
                # Create format for printing the title
                firstName = formattedY["first_name"]
                secondName = formattedY["second_name"]
                gameweekSummaryTitle = f"// Player summary: {firstName} {secondName}"
                underline = "-" * len(gameweekSummaryTitle)

                # Print the data with the title
                
                # TODO: Add in other metrics including ones we want to calculate
                
                print("")
                print(underline)
                print(gameweekSummaryTitle)
                print(underline)
                print("Total points: " + str(formattedY["total_points"]))
                print("Transfers in: " + str(formattedY["transfers_in"]))
                print("Transfers out: " + str(formattedY["transfers_out"]))
                print("// Net Transfers: " + str(int(formattedY["transfers_in"] - formattedY["transfers_out"])))
                print("Transfers in for gameweek: " + str(formattedY["transfers_in_event"]))
                print("Transfers out for gameweek: " + str(formattedY["transfers_out_event"]))
                print("// Net Transfers for gameweek: " + str(int(formattedY["transfers_in_event"] - formattedY["transfers_out_event"])))
                print("")
                playerInApi = True
                break

        elif playerSurname == "":
                print("")
                print("============================================================================")
                print("!! ERROR: No input won't work - you need a gameweekSummary surname:")
                print("============================================================================")
                playerSurname = str.lower(input("Try again:"))
                playerInfoBySurname(playerSurname)

    if playerInApi == False:
        print("")
        print("===============================================================")
        print(f"!! ERROR:Player not found - {secondName} - please check spelling and try again:")
        print("===============================================================")
        print("")
        playerInApi = True
        playerSurname = str.lower(input("Try again:"))
        playerInfoBySurname(playerSurname)

# Generates a list of player ID's and the associated player name as the key
def generatePlayerIDs():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDs = list()
    
    gameweekSummarySub = "bootstrap-static/"

    url = mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = generateJSONDumpsReadable(url)
    
    # Get all of the player id's
    for ids in gameweekSummaryDataReadable['elements']:
        dumpsIds = json.dumps(ids)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(ids,dict):
            formattedIds = json.loads(dumpsIds)
            currentPlayerID = formattedIds['id']
            playerIDs.append(currentPlayerID)
    playerIDs.sort()
    return playerIDs
    
# Pulls up the top 10 net transfers in
def mostNetTransfersIn(numberToDisplayUpTo):
    netTransfersByPlayer = dict()

    gameweekSummarySub = "bootstrap-static/"

    url = mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = generateJSONDumpsReadable(url)

    for data in gameweekSummaryDataReadable['elements']:
        dumpsIds = json.dumps(data)
        formattedIds = json.loads(dumpsIds)
        firstName = formattedIds['first_name']
        secondName = formattedIds['second_name']
        fullName = f'{firstName} {secondName}'
        transfersIn = formattedIds['transfers_in_event']
        transfersOut = formattedIds['transfers_out_event']
        netTransfers = transfersIn - transfersOut
        netTransfersByPlayer[fullName] = netTransfers

    sortedNetTransfers = list(reversed(sorted(netTransfersByPlayer.items(), key = lambda x : x[1])))

    topIndex = 0
    x = numberToDisplayUpTo - 1
    top10MostTransferedIn = list()

    while topIndex <= x:
         top10MostTransferedIn.append(sortedNetTransfers[topIndex])
         topIndex = topIndex + 1

    return top10MostTransferedIn

# Pulls up the top 10 net transfers out
def mostNetTransfersOut(numberToDisplayUpTo):
    netTransfersByPlayer = dict()

    gameweekSummarySub = "bootstrap-static/"

    url = mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = generateJSONDumpsReadable(url)

    for data in gameweekSummaryDataReadable['elements']:
        dumpsIds = json.dumps(data)
        formattedIds = json.loads(dumpsIds)
        firstName = formattedIds['first_name']
        secondName = formattedIds['second_name']
        fullName = f'{firstName} {secondName}'
        transfersIn = formattedIds['transfers_in_event']
        transfersOut = formattedIds['transfers_out_event']
        netTransfers = transfersIn - transfersOut
        netTransfersByPlayer[fullName] = netTransfers

    sortedNetTransfers = list(sorted(netTransfersByPlayer.items(), key = lambda x : x[1]))

    bottomIndex = 0
    x = numberToDisplayUpTo - 1
    top10MostTransferedOut = list()

    while bottomIndex <= x:
         top10MostTransferedOut.append(sortedNetTransfers[bottomIndex])
         bottomIndex = bottomIndex + 1

    return top10MostTransferedOut

# Creates all data for a given gameweek: 
def generateDataForGameWeek(gameweekNumber):
    playerIDs = generatePlayerIDs()
    # create url's for the current player and extract data from the "History" file where the game week is the current game week
    length = len(playerIDs) - 1
    elementsList = dict()
    tempList = list()
    # Gather the player data
    for playerID in playerIDs:
        currentIndex = list(playerIDs).index(playerID)
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"Gather data for gameweek {gameweekNumber}: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"Data for gameweek {gameweekNumber} gathered: 100%")
            sys.stdout.flush()
            print("")

        allPlayerDataReadable = generateJSONDumpsReadable(mergeURL('element-summary/')+str(playerID)+'/')

        currentList = dict()

        for data in allPlayerDataReadable['history']:        
            dumpsData = json.dumps(data)
            formattedData = json.loads(dumpsData)
            if gameweekNumber == formattedData['round']:
                for record in formattedData:
                    currentRound = formattedData['round']
                    currentList[record] = formattedData[record]
                # Create data list for current player assigning to each key
                for element in currentList:
                    if element not in elementsList:
                        elementsList[element] = (currentList[element])
                    else:
                        elementsList[element] = str(elementsList[element]) + ',' + str(currentList[element])
                currentList = dict()

    return elementsList