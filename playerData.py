import json
import csv 
import urllib.parse
import tkinter
import datetime
import math

import gameweekSummary
import genericMethods
import Teams
import playerData
import sqlFunction

from datetime import date
today = date.today()

def gameweeksPlayed(playerID):
    allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('element-summary/')+str(playerID)+'/')
    gameweeksPlayed = list()
    for data in allPlayerDataReadable['history']:
            gameweeksPlayed.append(int(data['round']))
    
    return gameweeksPlayed

# Create player first & last name list (and associated dictionary)
def generatePlayersFullNameList():

    gameweekSummaryListFull = list()
        
    dbConnect = sqlFunction.connectToDB("jackbegley","Athome19369*", "2021_2022_bootstrapstatic")
    cursor = dbConnect.cursor(dictionary=True)
    cursor.execute("SELECT CONCAT( first_name,' ', second_name ) AS fullname  FROM `2021_2022_bootstrapstatic`.`elements`")
    for row in cursor:
        gameweekSummaryListFull.append(row['fullname'])

    return gameweekSummaryListFull

# Create player id list
def generatePlayersIdsList():

    playerIDList = list()

    dbConnect = sqlFunction.connectToDB("jackbegley","Athome19369*", "2021_2022_bootstrapstatic")
    cursor = dbConnect.cursor(dictionary=True)
    cursor.execute("SELECT id  FROM `2021_2022_bootstrapstatic`.`elements`")
    for row in cursor:
        playerIDList.append(row['id'])
    
    return playerIDList

# Create player id list (and associated surname as the key)
def generatePlayerIDToSurnameMatching():
    
    playerIDMatchList = dict()

    dbConnect = sqlFunction.connectToDB("jackbegley","Athome19369*", "2021_2022_bootstrapstatic")
    cursor = dbConnect.cursor(dictionary=True)
    cursor.execute("SELECT id, second_name  FROM `2021_2022_bootstrapstatic`.`elements`")
    for row in cursor:
        secondName = row['second_name']
        cleanedSurname = str.lower(genericMethods.unicodeReplace(secondName))
        playerIDMatchList[cleanedSurname] = row['id']

    return playerIDMatchList

# Create player id as key and associated surname as the result
def generatePlayerIDAsKeySurnameAsResult():
    
    playerIDMatchList = dict()

    dbConnect = sqlFunction.connectToDB("jackbegley","Athome19369*", "2021_2022_bootstrapstatic")
    cursor = dbConnect.cursor(dictionary=True)
    cursor.execute("SELECT id, second_name  FROM `2021_2022_bootstrapstatic`.`elements`")
    for row in cursor:
        secondName = row['second_name']
        cleanedSurname = str.lower(genericMethods.unicodeReplace(secondName))
        playerIDMatchList[row['id']] = cleanedSurname

    return playerIDMatchList


# Create player id list (and associated surname as the key)
def generatePlayerIDToFullNameMatching():
    
    playerIDMatchList = dict()

    dbConnect = sqlFunction.connectToDB("jackbegley","Athome19369*", "2021_2022_bootstrapstatic")
    cursor = dbConnect.cursor(dictionary=True)
    cursor.execute("SELECT CONCAT( first_name,' ', second_name ) AS fullname  FROM `2021_2022_bootstrapstatic`.`elements`")
    for row in cursor:
        secondName = row['second_name']
        cleanedSurname = str.lower(genericMethods.unicodeReplace(secondName))
        playerIDMatchList[cleanedSurname] = row['id']

    return playerIDMatchList

# Create teamId list (and associated player id as key)
def generateIDAsKeyTeamIdAsValue():
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
            playerId = formattedY['id']
            teamID = formattedY['team']
            playerIDMatchList[playerId] = teamID

    return playerIDMatchList

# Return the chance of a player playing for next week, with the playerId as key
def generateChanceOfPlaying():
    players = genericMethods.generateJSONDumpsReadable('https://fantasy.premierleague.com/api/bootstrap-static/')
    chanceDict = dict()
    for player in players['elements']:
        if player['chance_of_playing_next_round'] == 'null':
            chance = 100

        if player['chance_of_playing_next_round'] == None:
            chance = 100
        else:
            chance = player['chance_of_playing_next_round']
        chanceDict[player['id']] = chance

    return chanceDict

# Match User input to an array and return the result
def matchUserInputToList(userInput, listToMatchInputTo):
    result = listToMatchInputTo[userInput]
    return result

# Create a filtered list where the arguments are passed in as a dictionary
def filterBootstrapStaticResults(filterField, filterValue, dictToFilter, operator):
    returnDict = dict()
    for player in dictToFilter:
        if isinstance(dictToFilter, list):
            if isinstance(filterValue, str) == True:
                if player[filterField] == filterValue:
                    returnDict[player['id']] = player
            else:
                    if (operator == '<' and player[filterField] < filterValue) or (operator == '=' and player[filterField] == filterValue) or (operator == '>' and player[filterField] > filterValue) or (operator == '>=' and player[filterField] >= filterValue) or (operator == '<=' and player[filterField] <= filterValue) or (operator == 'in' and player[filterField] in filterValue):
                        returnDict[player['id']] = player
        else:
            if isinstance(filterValue, str) == True:
                if dictToFilter[player][filterField] == filterValue:
                    returnDict[player] = dictToFilter[player]
            else:
                    if (operator == '<' and dictToFilter[player][filterField] < filterValue) or (operator == '=' and dictToFilter[player][filterField] == filterValue) or (operator == '>' and dictToFilter[player][filterField] > filterValue) or (operator == '>=' and dictToFilter[player][filterField] >= filterValue) or (operator == '<=' and dictToFilter[player][filterField] <= filterValue) or (operator == 'in' and dictToFilter[player][filterField] in filterValue):
                        returnDict[player] = dictToFilter[player]

    return returnDict

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
        genericMethods.runPercentage(length, currentIndex, "Gather data for regression", "Data for regression gathered")

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
    playerNames = playerData.generatePlayerIDToFullNameMatching()
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
        genericMethods.runPercentage(length, currentIndex, "Calculating player index", "Player index calculation completed")
        
        allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('element-summary/')+str(playerID)+'/')

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
        genericMethods.runPercentage(length, currentIndex, "Gathering data by player", "Data by player name gathered")

        for element in gameweekSummaryDataReadable['elements']:
            if playerID == element['id']:
                firstName = genericMethods.unicodeReplace(element['first_name'])
                secondName = genericMethods.unicodeReplace(element['second_name'])
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
            genericMethods.runPercentage(length, currentIndex, "Compiling exportable data file", "Exportable data file ready for use")

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


# Export the player data by gameweek where the playerID's have been gathered
def generateAllDataForAllYears(playerIDs):
    allDataByPlayer = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    summaryDataReadable = genericMethods.generateJSONDumpsReadable(url)
    positions = playerData.generatePlayerListwithPlayerCodeAsKey()

    for playerID in playerIDs:
        currentPlayerURL = genericMethods.mergeURL('element-summary/')+str(playerID)+'/'
        allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(currentPlayerURL)
        
        currentPlayerList = dict()
        
        currentIndex = list(playerIDs).index(playerID)
        length = len(playerIDs) - 1
        genericMethods.runPercentage(length, currentIndex, "Gathering data by player", "Data by player name gathered")

        for element in summaryDataReadable['elements']:
            if playerID == element['id']:
                firstName = genericMethods.unicodeReplace(element['first_name'])
                secondName = genericMethods.unicodeReplace(element['second_name'])
                position = element['element_type']
                fullName = f'{firstName} {secondName}'
                currentPlayerURL = genericMethods.mergeURL('element-summary/')+str(playerID)+'/'
                allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(currentPlayerURL)
                currentPlayerList = dict()                
                seasonDict = dict()
                for data in allPlayerDataReadable['history_past']:
                    dumpsData = json.dumps(data)
                    formattedData = json.loads(dumpsData)
                    currentDict = dict()
                    season = formattedData['season_name']
                    formattedData['position'] = position
                    for element in formattedData:
                        currentDict[element] = formattedData[element]
                    seasonDict[season] = currentDict
                    seasonDict['position'] = position
                if seasonDict:
                    allDataByPlayer[fullName] = seasonDict

               
    return allDataByPlayer

def exportDictionaryOfDataToExcel(dictionary):
    # Open a window allowing the user to specify the file save path using a File Explorer
    root = tkinter.Tk()
    savePath =tkinter.filedialog.askdirectory()
    root.destroy()
    # Get the file path
    fileName = input("What do you want to call the file? > ")
    filePath = f"{savePath}/{today} - {fileName}.csv"
    # Create the dictionaries for the data that we are going to print into csv
    exportList = dict()
    headerList = list()
    headerList.append('Full_name')
    headerList.append('gameweek')
    printed = 0

    # Open the csv with our file name and path so we can write in the data
    with open(filePath, 'w', newline='', encoding='utf-8') as out:
        # Create the csv writers with the settings we want (e.g. the different delimiters)
        csv_out_tab_seperator = csv.writer(out, delimiter="\t")
        csv_out_comma_seperator = csv.writer(out, delimiter=",")

        for key in dictionary:
            length = len(dictionary)-1
            currentIndex = list(dictionary).index(key)
            keyClean = key.strip().replace("'","`")
            genericMethods.runPercentage(length, currentIndex, "Compiling exportable data file", "Exportable data file ready for use")

            for season in dictionary[key]:
                seasonData = dictionary[key][season]
                for data in seasonData:
                    if data not in headerList:
                        headerList.append(data)
                    else:
                        if printed != 1:
                            csv_out_comma_seperator.writerow(headerList)
                            printed = 1

            for season in dictionary[key]:
                seasonData = dictionary[key][season]
                currentList = list()
                currentList.append(season)
                for data in seasonData:
                    currentAddition = str(seasonData[data]).strip()
                    currentList.append(currentAddition)
                exportList[key] = currentList
                exportListAsString = str(exportList[key]).replace("'","")
                exportableData = exportListAsString.replace('[','').replace(']','').replace('"',"")
                csv_out_tab_seperator.writerow([f'{keyClean},{exportableData}'])
    print("Done")



# Creates a list for the r value of each attribute in a correlation list
def rValuesPerField(correlationDictByAttribute):
    attributeRValues = dict()
    for attribute in correlationDictByAttribute:
        currentRValue = correlationDictByAttribute[attribute][2]
        attributeRValues[attribute] = currentRValue
    return attributeRValues

# Takes a number of seperate methods and creates a prediction on player performance for a specified week - TODO: UN-BREAK THIS
def predictPlayerPerformanceByGameweek(currentGameweek, previousGameweek):
    gameweekData = gameweekSummary.generateDataForGameWeek(previousGameweek)
    gameweekCurrentData = gameweekSummary.generateDataForGameWeek(currentGameweek)
    # Generate the Correlation Coefficient list
    currentRList = playerData.generateCorrelCoeffToPredictPerfomanceBasedOnPastWeekOnly(gameweekData, gameweekCurrentData, currentGameweek)
    # Apply correlation data to metrics for current Gameweek to estimate this weeks performance
    minList = playerData.calculateMinNumberInArray(allDataForCurrentGameWeek)
    maxList = playerData.calculateMaxNumberInArray(allDataForCurrentGameWeek)
    currentGameweek += 1
    dataByPlayerForCurrentWeek = playerData.gatherGameweekDataByPlayer(currentGameweek)
    indexedData = genericMethods.indexDataInADictionary(dataByPlayerForCurrentWeek, maxList, minList)
    finalIndexedPlayerDataWithCorrel = playerData.createPlayerIndexing(indexedData, currentRList)
    # Combine correlation scores between previous data and current total points scored
    maxNumberPlayers = playerData.calculateMaxNumberInArray(finalIndexedPlayerDataWithCorrel)
    minNumberPlayers = playerData.calculateMinNumberInArray(finalIndexedPlayerDataWithCorrel)
    # Index final scores to give an indication of performance
    finalIndexedPlayerDataIndexed = genericMethods.indexDataInADictionary(finalIndexedPlayerDataWithCorrel, maxNumberPlayers, minNumberPlayers)
    sortedFinalIndexedData = sorted(finalIndexedPlayerDataIndexed.items(), key=lambda x: x[1], reverse=True)
    return sortedFinalIndexedData

# Takes the correlations for the factors used to predict good performance and applies them to known top performers
def playerPerformanceForLastWeek(gameweekNumber):
    elementsList = playerData.gatherHistoricalPlayerData()
    allData = playerData.convertStringDictToInt(elementsList)
    # Correl needs to be updated to previous week vs current total points - method for generating that?
    correl = genericMethods.correlcoeffGeneration(allData,'total_points')
    currentRList = playerData.rValuesPerField(correl)
    minList = playerData.calculateMinNumberInArray(allData)
    maxList = playerData.calculateMaxNumberInArray(allData)
    # Data by player by week current and previous indexed
    gameweekNumber += 1
    dataByPlayerForWeek = playerData.gatherGameweekDataByPlayer(gameweekNumber)
    indexedData = genericMethods.indexDataInADictionary(dataByPlayerForWeek, maxList, minList)
    finalIndexedPlayerDataWithCorrel = playerData.createPlayerIndexing(indexedData, currentRList)
    # Combine correlation scores between previous data and current total points scored
    maxNumberPlayers = playerData.calculateMaxNumberInArray(finalIndexedPlayerDataWithCorrel)
    minNumberPlayers = playerData.calculateMinNumberInArray(finalIndexedPlayerDataWithCorrel)
    # Index final scores to give an indication of performance
    finalIndexedPlayerDataIndexed = genericMethods.indexDataInADictionary(finalIndexedPlayerDataWithCorrel, maxNumberPlayers, minNumberPlayers)
    sortedFinalIndexedData = sorted(finalIndexedPlayerDataIndexed.items(), key=lambda x: x[1], reverse=True)
    return sortedFinalIndexedData

# Player performance with correlation
def playerPerformanceWithCorrel(gameweekNumber, listOfRValues):
    allDataForCurrentGameweek = gameweekSummary.generateDataForGameWeek(gameweekNumber)
    minList = playerData.calculateMinNumberInArray(allDataForCurrentGameweek)
    maxList = playerData.calculateMaxNumberInArray(allDataForCurrentGameweek)
    dataByPlayerForWeek = playerData.gatherGameweekDataByPlayer(gameweekNumber)
    indexedData = genericMethods.indexDataInADictionary(dataByPlayerForWeek, maxList, minList)
    finalIndexedPlayerDataWithCorrel = playerData.createPlayerIndexing(indexedData, listOfRValues)
    maxNumberPlayers = playerData.calculateMaxNumberInArray(finalIndexedPlayerDataWithCorrel)
    minNumberPlayers = playerData.calculateMinNumberInArray(finalIndexedPlayerDataWithCorrel)
    # Index final scores to give an indication of performance
    finalIndexedPlayerDataIndexed = genericMethods.indexDataInADictionary(finalIndexedPlayerDataWithCorrel, maxNumberPlayers, minNumberPlayers)
    sortedFinalIndexedData = sorted(finalIndexedPlayerDataIndexed.items(), key=lambda x: x[1], reverse=True)

    return sortedFinalIndexedData

# Measures the prediction power of the previous weeks data on the current week and generates a correlation coefficient for each field in the data
def generateCorrelCoeffToPredictPerfomanceBasedOnPastWeekOnly(arrayToBaseCorrelationOffLastGameweek, arrayToBaseCorrelationOffThisGameweek, gameweekWeWantToPredictThePerformanceOf):
    currentGameweek = gameweekWeWantToPredictThePerformanceOf
    previousGameweek = currentGameweek - 1
    totalPointsCurrentWeek =  genericMethods.generateSingleEntryDictFromDict(arrayToBaseCorrelationOffThisGameweek, 'total_points')
    correl = genericMethods.correlcoeffGenerationForPrediction(arrayToBaseCorrelationOffLastGameweek, totalPointsCurrentWeek)
    currentRList = playerData.rValuesPerField(correl)
    return currentRList

# Measures the prediction power of the previous weeks data on the current week and generates a correlation coefficient for each field in the data
def generateCorrelCoeffToPredictPerfomanceBasedOnPastWeek(arrayToBaseCorrelationOffIncludingLastGameweek, gameweekWeWantToPredictThePerformanceOf):
    currentGameweek = gameweekWeWantToPredictThePerformanceOf + 1
    previousGameweek = gameweekWeWantToPredictThePerformanceOf
    allDataForPreviousGameWeek = arrayToBaseCorrelationOffIncludingLastGameweek[previousGameweek]
    totalPointsCurrentWeek =  genericMethods.generateSingleEntryDictFromDict(allDataForPreviousGameWeek , 'total_points')
    correl = genericMethods.correlcoeffGenerationForPrediction(allDataForPreviousGameWeek, totalPointsCurrentWeek)
    currentRList = playerData.rValuesPerField(correl)
    return currentRList

# Creates a list of the positions
def generatePositionReference():
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    positionsDict = dict()
    for data in currentDumps['element_types']:
        for key in data:
            positionName = str.lower(data['singular_name'])
            positionsDict[positionName] = data['id']
            break

    return positionsDict

# Creates a list of the positions
def generatePositionReferenceIDAsKey():
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    positionsDict = dict()
    for data in currentDumps['element_types']:
        for key in data:
            positionID = int(data['id'])
            positionsDict[positionID] = data['singular_name']
            break

    return positionsDict

# Creates a list of the players and their price
def generateListOfPlayersPricesInTeamByPosition(positionOfPlayers, idOfTeam):
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    playerCosts = list()
    for key in currentDumps['elements']:
        if key['element_type'] == positionOfPlayers and key['team'] == idOfTeam:
            playerCosts.append(key['now_cost'])

    return playerCosts

# Creates a list of the players and filter by price
def generateListOfPlayersByPositionByCost():
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    allPlayers = dict()
    GK = dict()
    DF = dict()
    MID = dict()
    FW = dict()
    for key in currentDumps['elements']:
        if key['element_type'] == 1:
            GK[key['id']] = key['now_cost']
        if key['element_type'] == 2:
            DF[key['id']] = key['now_cost']
        if key['element_type'] == 3:
            MID[key['id']] = key['now_cost']
        if key['element_type'] == 4:
            FW[key['id']] = key['now_cost']

    allPlayers[1] = GK
    allPlayers[2] = DF
    allPlayers[3] = MID
    allPlayers[4] = FW

    return allPlayers

# Creates a list of the players and their price
def generateListOfPlayersPrices():
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    playerCosts = dict()
    for key in currentDumps['elements']:
        playerCosts[key['id']] = key['now_cost']

    return playerCosts

# Generate a list of historical results by player position:
def generateHistoricalDataByPositionByPlayer():
    playerIDs = gameweekSummary.generatePlayerIDs()
    allDataByYear = generateAllDataForAllYears(playerIDs)
    positions = generatePositionReferenceIDAsKey()
    playerDataByPosition = dict()
    for position in positions:
        playersForPosition = dict()
        for player in allDataByYear:
            if allDataByYear[player]['position'] == position:
                currentPlayerData = dict()
                for data in allDataByYear[player]:
                    if data != 'position':
                        currentPlayerData[data] = allDataByYear[player][data]
                playersForPosition[player] = currentPlayerData
        playerDataByPosition[position] = playersForPosition

    return playerDataByPosition

# Generate position list with player code as key
def generatePlayerListwithPlayerCodeAsKey():
    playerKeys = dict()
    bootstrapDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    for player in bootstrapDumps['elements']:
        playerKeys[player['code']] = player['element_type']

    return playerKeys

# Creates a list of the players points
def generateListOfPlayersPointsInTeamByPosition(positionOfPlayers, idOfTeam):
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    playerPoints = list()
    for key in currentDumps['elements']:
        if key['element_type'] == positionOfPlayers and key['team'] == idOfTeam:
            playerPoints.append(key['total_points'])

    return playerPoints

# Creates a list of the players points per pound by players by position
def generateListOfPointsPerPoundPerPlayerPerPosition():
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    playerPointsGoalkeeper = dict()
    playerPointsDefender = dict()
    playerPointsMidfielder = dict()
    playerPointsForward = dict()
    pointsByPosition = dict()
    for key in currentDumps['elements']:
        if key['element_type'] == 1:
            player = key['id']
            playerPointsGoalkeeper[player] = (key['total_points']/(key['now_cost']/10))
        if key['element_type'] == 2:
            player = key['id']
            playerPointsDefender[player] = (key['total_points']/(key['now_cost']/10))
        if key['element_type'] == 3:
            player = key['id']
            playerPointsMidfielder[player] = (key['total_points']/(key['now_cost']/10))
        if key['element_type'] == 4:
            player = key['id']
            playerPointsForward[player] = (key['total_points']/(key['now_cost']/10))

    pointsByPosition[1] = playerPointsGoalkeeper
    pointsByPosition[2] = playerPointsDefender
    pointsByPosition[3] = playerPointsMidfielder
    pointsByPosition[4] = playerPointsForward

    return pointsByPosition

# Creates a list of points for a given player for a given range of weeks
def generateListOfPointsForNGameweeksPerPlayer(playerID, gameweekOfInterest, maxGameweek, maxValue, stringOrIntForNull):
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL(f'element-summary/{playerID}/'))
    gamesPlayed = gameweeksPlayed(playerID)
    currentPlayersPoints = list()
    weeksWeCareAbout = list()
    previousGameweek = 1
    n = gameweekOfInterest
    maxReached = False
    currentGameweek = genericMethods.generateCurrentGameweek()
    while n <= maxGameweek:
        weeksWeCareAbout.append(n)
        n += 1
    for data in currentDumps['history']:
        successful = False
        currentGameweek = int(data['round'])
        difference = currentGameweek - previousGameweek
        if int(gameweekOfInterest) <= int(data['round']) <= int(maxGameweek) and float(data['value']) <= maxValue * 10:
            if difference <= 1:
                if int(data['round']) in weeksWeCareAbout:
                    currentPlayersPoints.append(int(data['total_points']))
                    successful = True
                else:
                    if stringOrIntForNull == 'string':
                        currentPlayersPoints.append('-')
                        successful = True
                    else:
                        currentPlayersPoints.append(int(0))
                        successful = True
            elif int(gameweekOfInterest) <= int(data['round']):
                if stringOrIntForNull == 'string':
                    currentPlayersPoints.append('-')
                    successful = True
                else:
                    currentPlayersPoints.append(int(0))
                    successful = True
                currentPlayersPoints.append(int(data['total_points']))
                successful = True
            else:
                if stringOrIntForNull == 'string':
                    currentPlayersPoints.append('-')
                    successful = True
                else:
                    currentPlayersPoints.append(int(0))
                    successful = True

        previousGameweek = int(data['round'])
        if currentGameweek == maxGameweek:
            maxReached = True

        if int(gameweekOfInterest) <= int(currentGameweek) <= int(maxGameweek) and float(data['value']) <= maxValue * 10 and maxReached == False and successful == False:
            if stringOrIntForNull == 'string':
                currentPlayersPoints.append('-')
            else:
                currentPlayersPoints.append(int(0))

    return currentPlayersPoints

# Returns the average minutes played by a player from the start to the gameweek of interest
def averageMinutesPlayed(playerID, gameweekOfInterest):
    dumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL(f'element-summary/{playerID}/'))
    playerMinutes = list()
    currentGameweek = 1
    while currentGameweek <= gameweekOfInterest:
        for data in dumps['history']:
            if data["round"] == currentGameweek:
                playerMinutes.append(data["minutes"])

        currentGameweek += 1

    return genericMethods.listAverage(playerMinutes)

# Creates a list of ICT index over a user defined period for all players
def generateHistoryOfICTForNGameweeks(numberOfGameweeks, route):
    players = dict()
    playerList = generatePlayerIDToFullNameMatching() 
    playerToTeam = generateIDAsKeyTeamIdAsValue()
    currentGameweek = genericMethods.generateCurrentGameweek() - 1
    gameweek = currentGameweek - numberOfGameweeks
    teamDifficulty = Teams.teamIDsAsKeysAndGameweekDifficultyAsList(gameweek,currentGameweek)
    teamDifficulties = dict()
    for team in teamDifficulty:
        gameweeks = genericMethods.generateCurrentGameweek() - 1
        currentTeamDifficulties = dict()
        for difficulty in teamDifficulty[team]:
            currentTeamDifficulties[gameweeks] = difficulty
            gameweeks = gameweeks - 1
        teamDifficulties[team] = currentTeamDifficulties
    maxLen = len(playerList)
    for playerName in playerList:
        playerICT = dict()
        playerID = playerList[playerName]
        playerDifficulties = teamDifficulties[playerToTeam[playerID]]
        currentIndex = list(playerList.keys()).index(playerName)
        genericMethods.runPercentage(maxLen, currentIndex, "Running through all players", "Player ICT data collected for all players")
        currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL(f'element-summary/{playerID}/'))
        gameweek = currentGameweek - numberOfGameweeks
        for data in currentDumps['history']:
            ICTDict = dict()
            if gameweek <= data['round'] <= currentGameweek:
                points = data['total_points']
                difficulty = playerDifficulties[(data['round'])]
                ICTDict[data['round']] = float(data['ict_index'])
                if route == 1:
                    ICTDict['comparative'] = difficulty
                if route == 2:
                    ICTDict['comparative'] = points
                playerICT[data['round']] = ICTDict
                gameweek += 1
        players[playerID] = playerICT
                  
    return players

# Takes a array of player data where the player ID is the Key and sorts it by position
def sortPlayerDataByPosition(arrayToSort):
    currentDumps = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('bootstrap-static/'))
    playerPointsGoalkeeper = dict()
    playerPointsDefender = dict()
    playerPointsMidfielder = dict()
    playerPointsForward = dict()
    pointsByPosition = dict()
    for player in arrayToSort:
        for key in currentDumps['elements']:
            if key['element_type'] == 1 and player == key['id']:
                player = key['id']
                playerPointsGoalkeeper[player] = arrayToSort[player]
            if key['element_type'] == 2 and player == key['id']:
                player = key['id']
                playerPointsDefender[player] = arrayToSort[player]
            if key['element_type'] == 3 and player == key['id']:
                player = key['id']
                playerPointsMidfielder[player] = arrayToSort[player]
            if key['element_type'] == 4 and player == key['id']:
                player = key['id']
                playerPointsForward[player] = arrayToSort[player]

    pointsByPosition[1] = playerPointsGoalkeeper
    pointsByPosition[2] = playerPointsDefender
    pointsByPosition[3] = playerPointsMidfielder
    pointsByPosition[4] = playerPointsForward

    return pointsByPosition

# TODO: REMOVE AND REPLACE WITH SQL
# Creates a list of the players and metrics related to their performance
def generateListOfPlayersAndMetricsRelatedToPerformance(playerID, currentGameweek):
        urlBase = 'https://fantasy.premierleague.com/api/'
        playerDict = dict()
        statsDict = dict()
        playerDataForWeek = dict() 
        urlToUse = str(f'{urlBase}event/{currentGameweek}/live')
        currentDumps = genericMethods.generateJSONDumpsReadable(urlToUse)
        for gameweekData in currentDumps['elements']:
            if gameweekData['id'] == playerID:
                for data in gameweekData:
                    if data == 'stats':
                        for key in gameweekData['stats']:
                            currentData =gameweekData['stats']
                            dataToAdd = currentData[key]
                            playerDataForWeek[key] = dataToAdd
                    if data == 'explain':
                        for gameweekStats in gameweekData[data]:
                            for stats in gameweekStats['stats']:
                                dataKey = stats['identifier']
                                dataToAdd = stats['points']
                                playerDataForWeek[dataKey] = dataToAdd
                            playerDict = playerDataForWeek


        return playerDict

# Returns the influence of each player in order for a given gameweek
def playerInfluence(gameweekOfInterest):
        urlBase = 'https://fantasy.premierleague.com/api/'
        playerDict = dict()
        currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}bootstrap-static/')     
        for gameweekData in currentDumps['elements']:
            influence = float(gameweekData['influence'])
            playerID = gameweekData['id']
            playerDict[playerID] = influence
        
        sortedInfluence = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
        playerInfluence = genericMethods.reformattedSortedTupleAsDict(sortedInfluence)

        return playerInfluence

# Returns the influence of each player with the player ID as a reference for a given timeframe
def playerInfluenceInAGivenTimeFrameByTeam(endGameweek, numberOfDaysToLookBack):
        urlBase = 'https://fantasy.premierleague.com/api/'
        teamDict = dict()
        teams = Teams.teamIDsAsKeysAndNamesAsData()
        maxLen = len(teams)
        for team in teams:
            currentLen = list(teams.keys()).index(team) + 1
            genericMethods.runPercentage(maxLen, currentLen, f"Running team {currentLen} of {maxLen}", "Data collected for all of the teams")
            playersInTeam = Teams.generateListOfPlayerIDsAsKeysForTeam(team)
            playerDict = dict() 
            for player in playersInTeam:
                dbConnect = sqlFunction.connectToDB("jackbegley","Athome19369*", "2021_2022_elementsummary")
                cursor = dbConnect.cursor(dictionary=True)
                cursor.execute(f"SELECT influence FROM `2021_2022_elementsummary`.`history` WHERE element = {player} and round > {endGameweek - numberOfDaysToLookBack};")
                data = list()
                for row in cursor:
                    data.append(row["influence"])
                playerDict[player] = sum(data)
            teamDict[team] =  playerDict

        return teamDict


# Returns the influence of each player in order for a given gameweek
def playerPerformanceFactor(gameweekOfInterest):
        urlBase = 'https://fantasy.premierleague.com/api/'
        playerDict = dict()
        currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}bootstrap-static/')    
        nextGameweek = gameweekOfInterest + 1
        teamGamweekDifficulty = Teams.teamIDsAsKeysAndGameweekDifficultyAsList(nextGameweek, nextGameweek)
        maxLen = len(currentDumps['elements'])
        for gameweekData in currentDumps['elements']:
            teamId = gameweekData['team']
            if isinstance(teamGamweekDifficulty[teamId][0], int) == True:
                gameweekFactor = 6 - int(teamGamweekDifficulty[teamId][0]) 
            else:
                gameweekFactor = 0
            ict = float(gameweekData['ict_index'])
            totalPoints = int(gameweekData['total_points'])
            minutes = int(gameweekData['minutes'])
            pointsPerMinute = totalPoints / minutes if minutes else 0
            factor = ict * pointsPerMinute * gameweekFactor
            playerID = gameweekData['id']
            genericMethods.runPercentage(maxLen, playerID, f"Running player {playerID} of {maxLen}", "Data collected for all of the teams")
            playerDict[playerID] = factor
        
        sortedFactor = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
        playerFactor = genericMethods.reformattedSortedTupleAsDict(sortedFactor)

        return playerFactor


# Time in minutes played divided by (90 * gameweek number) = % time played

def percentageTimePlayedByPlayer():
        playerDict = dict()
        playerNames = generatePlayerIDAsKeySurnameAsResult()
        currentGameweek = genericMethods.generateCurrentGameweek()
        maxTime = currentGameweek * 90
        currentDumps = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/bootstrap-static/')   
        for gameweekData in currentDumps['elements']:
            playerID = gameweekData['id']
            name = playerNames[playerID].capitalize()
            minutes = int(gameweekData['minutes'])
            percentagePlayed = round((minutes / maxTime)*100,1)
            playerDict[name] = percentagePlayed

        return playerDict

# Total goal involvement by the players

def playerGoalInvolvement():
    playerDict = dict()
    playerNames = generatePlayerIDAsKeySurnameAsResult()
    currentDumps = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/bootstrap-static/')   
    for gameweekData in currentDumps['elements']:
        tempDict = dict()
        playerID = gameweekData['id']
        name = playerNames[playerID].capitalize()
        goals = int(gameweekData['goals_scored'])
        assists = int(gameweekData['assists'])
        involvement = goals + assists
        tempDict["name"] = name
        tempDict["involvement"] = involvement
        tempDict["goals"] = goals
        tempDict["assists"] = assists
        playerDict[playerID] = tempDict

    return playerDict

# Points per percentage selected

def pointsPerSelectedPercentage(minimumPercentageSelected, maximumCost, minimumCost):
    playerDict = dict()
    playerNames = generatePlayerIDAsKeySurnameAsResult()
    currentGameweek = genericMethods.generateCurrentGameweek()
    currentDumps = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/bootstrap-static/')   
    length = len(currentDumps['elements'])
    for gameweekData in currentDumps['elements']:
        currentIndex = currentDumps['elements'].index(gameweekData)    
        genericMethods.runPercentage(length, currentIndex, "Generating points per percentage selected dictionary", f"Dictionary created for all players up to £{maximumCost}M values and selected by {minimumPercentageSelected}%")
        tempDict = dict()
        playerID = gameweekData['id']
        name = playerNames[playerID].capitalize()
        points = int(gameweekData['total_points'])
        history = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/element-summary/{playerID}/')['history']
        numberOfGames = len(history)
        if numberOfGames > 0:
            for record in history:
                if int(record['round']) == (currentGameweek - 1):
                    value = record['value'] / 10
            selected = float(gameweekData['selected_by_percent'])
            if selected < minimumPercentageSelected:
                pointsPerPercentage = 0 
            else:
                pointsPerPercentage = points / selected if selected else 0 
            tempDict["name"] = name
            tempDict["pointsPerPercent"] = pointsPerPercentage
            tempDict["points"] = points
            tempDict["selected"] = selected
            tempDict["value"] = value
            tempDict["goals"] = int(gameweekData['goals_scored'])
            tempDict["assists"] = int(gameweekData['assists'])
            tempDict["bonus"] = int(gameweekData['bonus'])
            tempDict["ict"] = float(gameweekData['ict_index'])
            tempDict["minutesPercentage"] = float((int(gameweekData['minutes']) / numberOfGames) / 90) * 100
            tempDict["pointsPerGame"] = float(gameweekData['points_per_game'])
            if minimumCost <= value <= maximumCost:
                playerDict[playerID] = tempDict

    return playerDict

def formatPlayerDataForGameweekRange(startGameweek, endGameweek, playerIDs):
    # create url's for the current player and extract data from the "History" file where the game week is the current game week
    length = len(playerIDs) - 1
    allPlayerData = dict()
    # Gather the player data
    for playerID in playerIDs:
        currentIndex = list(playerIDs).index(playerID)
        playerHistory = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('element-summary/')+str(playerID)+'/')['history']
        genericMethods.runPercentage(length, currentIndex, f"Formatting data for player {currentIndex} of {length}", f"Data for all players has been formatted")
        currentGameweek = startGameweek
        currentPlayerData = dict()
        while currentGameweek <= endGameweek:
            allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('element-summary/')+str(playerID)+'/')
            for data in allPlayerDataReadable['history']:        
                if currentGameweek == data['round']:
                    currentPlayerData[int(currentGameweek)] = data
                    break

            currentGameweek += 1
        allPlayerData[playerID] = currentPlayerData

    return allPlayerData

def playedAGameweekOfInterest(startGameweek, endGameweek, playerID):
    n = startGameweek
    gwRange = list()
    while n <= endGameweek:
        gwRange.append(n)
        n += 1
    allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('element-summary/')+str(playerID)+'/')
    for data in allPlayerDataReadable['history']:
        if data['round'] in gwRange:
            return data['round']
    return False