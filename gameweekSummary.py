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

# Create player first & last name list (and associated dictionary)
def playersListFunction():

    # Initialise the arrays outside the loop so that they cannot be overriden
    gameweekSummaryListFull = list()
    gameweekSummaryListSecond = list()

    
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
            firstName = formattedY['first_name']
            secondName = formattedY['second_name']
            secondNameNoLead = secondName.lstrip()
            fullName = f'{firstName} {secondName}'
            gameweekSummaryListFull.append(fullName)
            gameweekSummaryListSecond.append(secondNameNoLead)

            # Print the options to the console   
            print("------------------------------------")
            print("How would you like to see the output?")
            print("------------------------------------")
            print(" [1] Full list")
            print(" [2] Comma seperated list  of surnames")
            print("------------------------------------")
            playerListInput = input(" > ")
            # try and put the input in as an integer
            parse(playerListInput)
            if isInt(playerListInput):
                if int(playerListInput) == 1:
                    for player in gameweekSummaryListFull:
                        print(player)
                        endRoutine()
                elif int(playerListInput) == 2:
                    gameweekSummaryListCleaned = str(gameweekSummaryListSecond).replace("'","").replace("[","").replace("]","")
                    print(gameweekSummaryListCleaned)
                    copyTo = Tk()
                    copyTo.clipboard_clear()
                    copyTo.clipboard_append(gameweekSummaryListCleaned)
                    copyTo.update()
                    copyTo.destroy()
                    print("")
                    print("// This has been copied to your clipboard.")
                    print("")
                    endRoutine()
                else:
                    print("======================================================================================")
                    print("!! ERROR:Command wasn't recognised- please pick one of the above options and try again:")
                    print("======================================================================================")
                    print("")
                    gameweekSummaryListFunction()

            else:
                print("====================================================================================")
                print("!! ERROR:Input was not a number - please pick one of the above options and try again:")
                print("====================================================================================")
                print("")
                gameweekSummaryListFunction()

        else:
            print("====================================================================================")
            print("!! ERROR: // Array not in correct format")
            print("====================================================================================")
            print("")
            endRoutine()

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
