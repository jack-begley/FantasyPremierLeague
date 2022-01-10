import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import requests
import json
import csv 
import urllib.parse
import tkinter
from tkinter import Tk
import playerData
import gameweekSummary
import genericMethods
import Teams

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

    url = genericMethods.mergeURL(gameweekSummarySub)
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

    url = genericMethods.mergeURL(urlAddOn)

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
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryJSON = requests.get(url)
    gameweekSummaryData = gameweekSummaryJSON.json()
    gameweekSummaryDataDumps = json.dumps(gameweekSummaryData)
    gameweekSummaryDataReadable = json.loads(gameweekSummaryDataDumps)

    gameweekNumber = genericMethods.generateCurrentGameweek()

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
                gameweekSummaryTitle = f"/ Player profile: {firstName} {secondName}"
                underline = "-" * len(gameweekSummaryTitle)

                # Print the data with the title
                
                # TODO: Add in other metrics including ones we want to calculate
                
                print("")
                print(gameweekSummaryTitle)
                print("")
                print("Selected %: " + str(formattedY["selected_by_percent"]) + "%")
                print("Form: " + str(formattedY["form"]))
                print("Avg. minutes played: " + str(round((formattedY["minutes"] / gameweekNumber), 0)))
                print("Influence: " + str(formattedY["influence"]))
                print("")
                print("/ Points:")
                print("")
                print("Total points: " + str(formattedY["total_points"]))
                print("")
                print("Goals scored: " + str(formattedY["goals_scored"]))
                print("Assists: " + str(formattedY["assists"]))
                print("Red cards: " + str(formattedY["red_cards"]))
                print("Yellow cards: " + str(formattedY["yellow_cards"]))
                print("Bonus points: " + str(formattedY["bonus"]))
                print("")
                print("Points per game: " + str(formattedY["points_per_game"]))
                playerInApi = True
                break

        elif playerSurname == "":
                print("")
                print("============================================================================")
                print("!! ERROR: No input won't work - you need a gameweekSummary surname:")
                print("============================================================================")
                playerSurname = str.lower(input("Try again:"))
                gameweekSummary.playerInfoBySurname(playerSurname)

    if playerInApi == False:
        print("")
        print("===============================================================")
        print(f"!! ERROR:Player not found - {secondName} - please check spelling and try again:")
        print("===============================================================")
        print("")
        playerInApi = True
        playerSurname = str.lower(input("Try again:"))
        gameweekSummary.playerInfoBySurname(playerSurname)

# Getting the information of a player based on their Id
def playerInfoById(playerId, position):

    gameweekSummarySub = "bootstrap-static/"

    # In order to either read in the index of the item, or the item name we either need the loaded version, or the dumped version respectively
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryJSON = requests.get(url)
    gameweekSummaryData = gameweekSummaryJSON.json()
    gameweekSummaryDataDumps = json.dumps(gameweekSummaryData)
    gameweekSummaryDataReadable = json.loads(gameweekSummaryDataDumps)

    gameweekNumber = genericMethods.generateCurrentGameweek()

    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        playerInApi = False
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            id = formattedY['id']

            #Generate a list for the headers
            if id == playerId:
                
                # Create format for printing the title
                firstName = formattedY["first_name"]
                secondName = formattedY["second_name"]
                gameweekSummaryTitle = f"/ Player profile: {firstName} {secondName}"
                underline = "-" * len(gameweekSummaryTitle)

                # Print the data with the title
                
                # TODO: Add in other metrics including ones we want to calculate
                
                performanceStatistics = list()

                if position == 1:
                    performanceStatistics.append("Clean sheets: " + str(formattedY["clean_sheets"]))
                    performanceStatistics.append("Penalties saved: " + str(formattedY["penalties_saved"]))
                    performanceStatistics.append("Total saves: " + str(formattedY["saves"]))
                    performanceStatistics.append("Total goals conceded: " + str(formattedY["goals_conceded"]))

                if position in [2,3]:
                    performanceStatistics.append("Clean sheets: " + str(formattedY["clean_sheets"]))
                    performanceStatistics.append("Goals: " + str(formattedY["goals_scored"]))
                    performanceStatistics.append("Assists: " + str(formattedY["assists"]))
                    performanceStatistics.append("Corners and indirect free kick order rank: " + str(formattedY["corners_and_indirect_freekicks_order"]))
                    performanceStatistics.append("Direct free kick order rank: " + str(formattedY["direct_freekicks_order"]))
                    performanceStatistics.append("Penalty order rank: " + str(formattedY["penalties_order"]))
                    performanceStatistics.append("Total goals conceded: " + str(formattedY["goals_conceded"]))

                if position == 4:
                    performanceStatistics.append("Goals: " + str(formattedY["goals_scored"]))
                    performanceStatistics.append("Assists: " + str(formattedY["assists"]))
                    performanceStatistics.append("Corners and indirect free kick order rank: " + str(formattedY["corners_and_indirect_freekicks_order"]))
                    performanceStatistics.append("Direct free kick order rank: " + str(formattedY["direct_freekicks_order"]))
                    performanceStatistics.append("Penalty order rank: " + str(formattedY["penalties_order"]))

                performanceStatistics.append("Red cards: " + str(formattedY["red_cards"]))
                performanceStatistics.append("Yellow cards: " + str(formattedY["yellow_cards"]))
                performanceStatistics.append("Bonus points: " + str(formattedY["bonus"]))

                teams = Teams.teamIDsAsKeysAndNamesAsData()

                print("")
                print(gameweekSummaryTitle)
                print("")
                print("/ Background:")
                print("")
                print("Value (£): " + "£" + str(formattedY["now_cost"]/10) + "M")
                print("Team: " + str(teams[formattedY["team"]]).capitalize())
                print("")
                print("Selected (%): " + str(formattedY["selected_by_percent"]) + "%")
                print("Form: " + str(formattedY["form"]))
                print("No. times in dreamteam: " + str(round((formattedY["dreamteam_count"]), 0)))
                print("Avg. minutes played: " + str(round((formattedY["minutes"] / gameweekNumber), 0)))
                print("ICT Index: " + str(formattedY["ict_index"]))
                print("ICT Rank overall: " + str(formattedY["ict_index_rank"]))
                print("ICT for position: " + str(formattedY["ict_index_rank_type"]))
                print("")
                print("/ Points:")
                print("")
                print("Total points: " + str(formattedY["total_points"]))
                print("")
                for stat in performanceStatistics:
                    print(stat)
                print("")
                print("Points per game: " + str(formattedY["points_per_game"]))
                print("")
                print("/ Expected points:")
                print("")
                print("Expected point last week: " + str(formattedY["ep_next"]))
                print("Expected points this week: " + str(formattedY["ep_this"]))
                print("")

                break

# Generates a list of player ID's and the associated player name as the key
def generatePlayerIDs():
    # Initialise the arrays outside the loop so that they cannot be overriden
    playerIDs = list()
    
    gameweekSummarySub = "bootstrap-static/"

    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)
    
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

    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

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
    numberToDisplayUpTo = int(numberToDisplayUpTo)
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

    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

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
    numberToDisplayUpTo = int(numberToDisplayUpTo)
    x = numberToDisplayUpTo - 1
    top10MostTransferedOut = list()

    while bottomIndex <= x:
         top10MostTransferedOut.append(sortedNetTransfers[bottomIndex])
         bottomIndex = bottomIndex + 1

    return top10MostTransferedOut

# Creates all data for a given gameweek: 
def generateDataForGameWeek(gameweekNumber):
    playerIDs = gameweekSummary.generatePlayerIDs()
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

        allPlayerDataReadable = genericMethods.generateJSONDumpsReadable(genericMethods.mergeURL('element-summary/')+str(playerID)+'/')

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


# Sums all data for a given gameweek range: 
def generateSumDataForGameWeekRange(startGameweek, endGameweek, playerIDs, fieldsOfInterest):
    # create url's for the current player and extract data from the "History" file where the game week is the current game week
    length = len(playerIDs) - 1
    allPlayerData = dict()
    # Gather the player data
    allData = playerData.formatPlayerDataForGameweekRange(startGameweek, endGameweek, playerIDs)
    gwRange = list()
    for playerID in playerIDs:
        interestingWeek = playerData.playedAGameweekOfInterest(startGameweek, endGameweek, playerID)
        if interestingWeek != False:
            currentIndex = list(playerIDs).index(playerID)
            sumFields = dict()
            n = 1
            genericMethods.runPercentage(length, currentIndex, f"Gather data for player {currentIndex} of {length}", f"Data for all players has been gathered")
            for field in fieldsOfInterest:
                fieldList = list()
                if field in allData[playerID][interestingWeek]:
                    currentGameweek = startGameweek
                    while currentGameweek <= endGameweek:
                        try:
                            fieldList.append(float(allData[playerID][currentGameweek][field]))
                        except:
                            fieldList.append(0.0)
                        currentGameweek += 1
                    
                sumValue = sum(fieldList)
                sumFields[field] = sumValue

            allPlayerData[playerID] = sumFields

        else: 
            break 

    return  allPlayerData