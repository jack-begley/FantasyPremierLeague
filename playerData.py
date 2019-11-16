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
from Teams import *

#Setting up url construction

def mergeURL(sub):
    return 'https://fantasy.premierleague.com/api/' + sub;
# Syntax e.g. = print(mergeURL(userSummary))

# URL set up and league codes
from datetime import date
today = date.today()

# All gameweek data for a player (by gameweek)
def allPlayerDataBySurname(playerSurname):
    playerID = matchUserInputToList(playerSurname,generatePlayerIDToSurnameMatching())
    currentGameWeek = math.floor((datetime.datetime.now() - datetime.datetime(2019, 8, 5)).days/7)
    elementsList = dict()
    tempList = list()
    allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(mergeURL('element-summary/')+str(playerID)+'/')
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

# Create player first & last name list (and associated dictionary)
def generatePlayersFullNameList():
    # Initialise the arrays outside the loop so that they cannot be overriden
    gameweekSummaryListFull = list()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

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

    return gameweekSummaryListFull

# Create player id list
def generatePlayersIdsList():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDList = list()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            id = formattedY['id']
            playerIDList.append(id)
    
    return playerIDList

# Create player id list (and associated surname as the key)
def generatePlayerIDToSurnameMatching():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDMatchList = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            secondName = formattedY['second_name']
            cleanedFullName = str.lower(unicodeReplace(secondName))
            id = formattedY['id']
            playerIDMatchList[cleanedFullName] = id

    return playerIDMatchList

# Create player id list (and associated surname as the key)
def generatePlayerIDToFullNameMatching():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDMatchList = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            firstName = formattedY['first_name']
            secondName = formattedY['second_name']
            fullName = f'{firstName} {secondName}'
            cleanedFullName = str.lower(unicodeReplace(fullName))
            id = formattedY['id']
            playerIDMatchList[cleanedFullName] = id

    return playerIDMatchList

# Create player name list (and associated name as key)
def generatePlayerNameToIDMatching():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDMatchList = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            secondName = formattedY['second_name']
            cleanedSecondName = str.lower(unicodeReplace(secondName))
            id = formattedY['id']
            playerIDMatchList[id] = cleanedSecondName

    return playerIDMatchList

# Create player name list (and associated id as key)
def generatePlayerNameToIDMatching():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDMatchList = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

    # For all of the objects in the readable player data list under the "elements" key (the name of a list)
    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        # Only run the below part if "y" is in the format of a dictionary (a list of data)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            secondName = formattedY['second_name']
            cleanedSecondName = str.lower(unicodeReplace(secondName))
            id = formattedY['id']
            playerIDMatchList[id] = cleanedSecondName

    return playerIDMatchList

# Match User input to an array and return the result
def matchUserInputToList(userInput, listToMatchInputTo):
    result = listToMatchInputTo[userInput]
    return result

# Create player first & last name list (and associated dictionary)
def gatherHistoricalPlayerData():
    playerIDs = gameweekSummary.generatePlayerIDs()
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

        allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('element-summary/')+str(playerID)+'/')

        currentPlayerList = dict()

        for data in allPlayerDataReadable['history']:        
            dumpsData = json.dumps(data)
            formattedData = json.loads(dumpsData)
            gameweek = formattedData['round']
            id = formattedData['element']
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

# Gather gameweek data specified
def gatherGameweekDataByPlayer(gameweekOfInterest):
    playerNames = generatePlayerIDToFullNameMatching()
    if gameweekOfInterest == None:
        currentGameWeek = math.floor((datetime.datetime.now() - datetime.datetime(2019, 8, 5)).days/7) - 1
    else:
        currentGameWeek = gameweekOfInterest
    length = len(playerNames) - 1
    playerDataFinal = dict()
    # Gather the player data
    for playerName in playerNames:
        playerID = playerNames[playerName]
        currentPlayerData = dict()
        currentIndex = list(playerNames).index(playerName)
        runPercentageComplete = str(round((currentIndex/length)*100,1))
        if runPercentageComplete != "100.0":
            sys.stdout.write('\r'f"Calculating player index: {runPercentageComplete}%"),
            sys.stdout.flush()
        else:
            sys.stdout.write('\r'"")
            sys.stdout.write(f"Player index calculation completed: 100%")
            sys.stdout.flush()
            print("")

        allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(mergeURL('element-summary/')+str(playerID)+'/')

        currentPlayerList = dict()

        for data in allPlayerDataReadable['history']:    
            if data['round'] == currentGameWeek:
                playerDataFinal[playerName] = data

    return playerDataFinal

# Calculate the Max number of a dictionary array
def calculateMaxNumberInArray(arrayToCalculateMaxFrom):
    dictOfMaxNumbersByKey = dict()
    try:
        for key in arrayToCalculateMaxFrom:
                maxNumbers = max(list(arrayToCalculateMaxFrom[key]))
                dictOfMaxNumbersByKey[key] = maxNumbers
        return dictOfMaxNumbersByKey
    
    except:
        tempList = list()
        for secondaryKey in arrayToCalculateMaxFrom:
            tempList.append(arrayToCalculateMaxFrom[secondaryKey])
        maxNumber = max(list(tempList))

        return maxNumber

# Calculate the Max number in a dictionary array
def calculateMinNumberInArray(arrayToCalculateMinFrom):
    dictOfMinNumbersByKey = dict()
    try:
        for key in arrayToCalculateMinFrom:
                minNumbers = min(list(arrayToCalculateMinFrom[key]))
                if minNumbers == ",":
                    minNumbers = 0
                dictOfMinNumbersByKey[key] = minNumbers
        return dictOfMinNumbersByKey
    
    except:
        tempList = list()
        for secondaryKey in arrayToCalculateMinFrom:
            tempList.append(arrayToCalculateMinFrom[secondaryKey])
        minNumber = min(list(tempList))
        if minNumber == "'":
            minNumber = 0

        return minNumber

# Multiply one factor by another where there are two dictionaries that have matching keys - Player and Correlation data
def createPlayerIndexing(dataToMatchToCorrelList, correlListWithMatchingKeys):
    finalPlayerIndex = dict()
    for player in dataToMatchToCorrelList:
        previousIndex = float()
        currentPlayerList = list()
        for key in dataToMatchToCorrelList[player]:
            currentIndex = float()
            if key != 'kickoff_time':
                currentPlayerData = dataToMatchToCorrelList[player]
                correlConstant = correlListWithMatchingKeys[key]
                currentData = float(currentPlayerData[key])
                currentIndex = correlConstant * currentData
                previousIndex = currentIndex + previousIndex
        finalPlayerIndex[player] =  previousIndex

    return finalPlayerIndex
        
# Converts a dictionary that is string based to an integer list
def convertStringDictToInt(inputList):
   # Get All data into integers in a comma seperated list
    outputList = dict()
    currentDict = dict()
    tempList = list()
    for element in inputList:
        try:
            outputList[element] = list(map(float, inputList[element].split(',')))
        except BaseException:
            if element != "kickoff_time":
                currentDict[element] = list(map(str, inputList[element].split(',')))
                for n in currentDict[element]:
                        n = int((n).replace('False', '0').replace('True', '1').replace('None', '-1'))
                        tempList.append(n)
                outputList[element] = tempList
                currentDict = dict()
                tempList = list()
            else:
                None
    return outputList

# Export the player data by gameweek where the playerID's have been gathered
def exportPlayerDataByGameweek(playerIDs):
    playerName = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

    for playerID in playerIDs:
        currentPlayerURL = genericMethods.mergeURL('element-summary/')+str(playerID)+'/'
        allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(currentPlayerURL)
        
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
                currentPlayerURL = genericMethods.mergeURL('element-summary/')+str(playerID)+'/'
                allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(currentPlayerURL)
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

# Creates a list for the r value of each attribute in a correlation list
def rValuesPerField(correlationDictByAttribute):
    attributeRValues = dict()
    for attribute in correlationDictByAttribute:
        currentRValue = correlationDictByAttribute[attribute][2]
        attributeRValues[attribute] = currentRValue
    return attributeRValues

# Takes a number of seperate methods and creates a prediction on player performance for a specified week
def predictPlayerPerformanceByGameweek(currentGameweek, previousGameweek):
    gameweekData = gameweekSummary.generateDataForGameWeek(previousGameweek)
    gameweekCurrentData = gameweekSummary.generateDataForGameWeek(currentGameweek)
    # Generate the Correlation Coefficient list
    currentRList = generateCorrelCoeffToPredictPerfomanceBasedOnPastWeekOnly(gameweekData, gameweekCurrentData, currentGameweek)
    # Apply correlation data to metrics for current Gameweek to estimate this weeks performance
    minList = calculateMinNumberInArray(allDataForCurrentGameWeek)
    maxList = calculateMaxNumberInArray(allDataForCurrentGameWeek)
    dataByPlayerForCurrentWeek = gatherGameweekDataByPlayer(currentGameweek)
    indexedData = genericMethods.indexDataInADictionary(dataByPlayerForCurrentWeek, maxList, minList)
    finalIndexedPlayerDataWithCorrel = createPlayerIndexing(indexedData, currentRList)
    # Combine correlation scores between previous data and current total points scored
    maxNumberPlayers = calculateMaxNumberInArray(finalIndexedPlayerDataWithCorrel)
    minNumberPlayers = calculateMinNumberInArray(finalIndexedPlayerDataWithCorrel)
    # Index final scores to give an indication of performance
    finalIndexedPlayerDataIndexed = genericMethods.indexDataInADictionary(finalIndexedPlayerDataWithCorrel, maxNumberPlayers, minNumberPlayers)
    sortedFinalIndexedData = sorted(finalIndexedPlayerDataIndexed.items(), key=lambda x: x[1], reverse=True)
    return sortedFinalIndexedData

# Takes the correlations for the factors used to predict good performance and applies them to known top performers
def playerPerformanceForLastWeek(gameweekNumber):
    elementsList = gameweekSummary.gatherHistoricalPlayerData()
    allData = convertStringDictToInt(elementsList)
    # Correl needs to be updated to previous week vs current total points - method for generating that?
    correl = correlcoeffGeneration(allData,'total_points')
    currentRList = rValuesPerField(correl)
    minList = calculateMinNumberInArray(allData)
    maxList = calculateMaxNumberInArray(allData)
    # Data by player by week current and previous indexed
    dataByPlayerForWeek = gatherGameweekDataByPlayer(gameweekNumber)
    indexedData = genericMethods.indexDataInADictionary(dataByPlayerForWeek, maxList, minList)
    finalIndexedPlayerDataWithCorrel = createPlayerIndexing(indexedData, currentRList)
    # Combine correlation scores between previous data and current total points scored
    maxNumberPlayers = calculateMaxNumberInArray(finalIndexedPlayerDataWithCorrel)
    minNumberPlayers = calculateMinNumberInArray(finalIndexedPlayerDataWithCorrel)
    # Index final scores to give an indication of performance
    finalIndexedPlayerDataIndexed = genericMethods.indexDataInADictionary(finalIndexedPlayerDataWithCorrel, maxNumberPlayers, minNumberPlayers)
    sortedFinalIndexedData = sorted(finalIndexedPlayerDataIndexed.items(), key=lambda x: x[1], reverse=True)
    return sortedFinalIndexedData

# Player performance with correlation
def playerPerformanceWithCorrel(gameweekNumber, listOfRValues):
    allDataForCurrentGameweek = gameweekSummary.generateDataForGameWeek(gameweekNumber)
    minList = calculateMinNumberInArray(allDataForCurrentGameweek)
    maxList = calculateMaxNumberInArray(allDataForCurrentGameweek)
    dataByPlayerForWeek = gatherGameweekDataByPlayer(gameweekNumber)
    indexedData = genericMethods.indexDataInADictionary(dataByPlayerForWeek, maxList, minList)
    finalIndexedPlayerDataWithCorrel = createPlayerIndexing(indexedData, listOfRValues)
    maxNumberPlayers = calculateMaxNumberInArray(finalIndexedPlayerDataWithCorrel)
    minNumberPlayers = calculateMinNumberInArray(finalIndexedPlayerDataWithCorrel)
    # Index final scores to give an indication of performance
    finalIndexedPlayerDataIndexed = genericMethods.indexDataInADictionary(finalIndexedPlayerDataWithCorrel, maxNumberPlayers, minNumberPlayers)
    sortedFinalIndexedData = sorted(finalIndexedPlayerDataIndexed.items(), key=lambda x: x[1], reverse=True)

    return sortedFinalIndexedData

# Measures the prediction power of the previous weeks data on the current week and generates a correlation coefficient for each field in the data
def generateCorrelCoeffToPredictPerfomanceBasedOnPastWeekOnly(arrayToBaseCorrelationOffLastGameweek, arrayToBaseCorrelationOffThisGameweek, gameweekWeWantToPredictThePerformanceOf):
    currentGameweek = gameweekWeWantToPredictThePerformanceOf
    previousGameweek = currentGameweek - 1
    totalPointsCurrentWeek =  generateSingleEntryDictFromDict(arrayToBaseCorrelationOffThisGameweek, 'total_points')
    correl = correlcoeffGenerationForPrediction(arrayToBaseCorrelationOffLastGameweek, totalPointsCurrentWeek)
    currentRList = rValuesPerField(correl)
    return currentRList

# Measures the prediction power of the previous weeks data on the current week and generates a correlation coefficient for each field in the data
def generateCorrelCoeffToPredictPerfomanceBasedOnPastWeek(arrayToBaseCorrelationOffIncludingLastGameweek, gameweekWeWantToPredictThePerformanceOf):
    currentGameweek = gameweekWeWantToPredictThePerformanceOf
    previousGameweek = currentGameweek - 1
    allDataForPreviousGameWeek = arrayToBaseCorrelationOffIncludingLastGameweek[previousGameweek]
    totalPointsCurrentWeek =  generateSingleEntryDictFromDict(allDataForPreviousGameWeek , 'total_points')
    correl = correlcoeffGenerationForPrediction(allDataForPreviousGameWeek, totalPointsCurrentWeek)
    currentRList = rValuesPerField(correl)
    return currentRList


# Creates a list of the positions
def generatePositionReference():
    currentDumps = genericMethods.generateJSONDumpsReadable(mergeURL('bootstrap-static/'))
    positionsDict = dict()
    for data in currentDumps['element_types']:
        for key in data:
            positionName = str.lower(data['singular_name'])
            positionsDict[positionName] = data['id']
            break

    return positionsDict

# Creates a list of the players and their price
def generateListOfPlayersPricesInTeamByPosition(positionOfPlayers, idOfTeam):
    currentDumps = genericMethods.generateJSONDumpsReadable(mergeURL('bootstrap-static/'))
    playerCosts = list()
    for key in currentDumps['elements']:
        if key['element_type'] == positionOfPlayers and key['team'] == idOfTeam:
            playerCosts.append(key['now_cost'])

    return playerCosts

# Creates a list of the players points
def generateListOfPlayersPointsInTeamByPosition(positionOfPlayers, idOfTeam):
    currentDumps = genericMethods.generateJSONDumpsReadable(mergeURL('bootstrap-static/'))
    playerPoints = list()
    for key in currentDumps['elements']:
        if key['element_type'] == positionOfPlayers and key['team'] == idOfTeam:
            playerPoints.append(key['total_points'])

    return playerPoints