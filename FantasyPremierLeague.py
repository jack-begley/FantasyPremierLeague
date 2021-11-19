import gameweekSummary
import playerData
import genericMethods
import detailedStats
import Teams
import sqlFunction
import operator
import requests
import tkinter as Tk
import sys, traceback
from collections import OrderedDict
import operator
import prettytable
from prettytable import PrettyTable

"""
The FPL module.

Autentication Guide: https://medium.com/@bram.vanherle1/fantasy-premier-league-api-authentication-guide-2f7aeb2382e4

https://fantasy.premierleague.com/api/my-team/{team-id}/
https://fantasy.premierleague.com/api/entry/{team-id}/
https://fantasy.premierleague.com/api/leagues-classic/{league-id}/standings/
https://fantasy.premierleague.com/api/leagues-h2h/{league-id}/standings/
https://fantasy.premierleague.com/api/entry/{team-id}/transfers-latest/

Fantasy Premier League API:
* /bootstrap-static [Y]
* /bootstrap-dynamic [N]
* /elements [N]
* /element-summary/{player_id} [Y]
* /entry/{user_id} [Y]
* /entry/{user_id}/cup [N]
* /entry/{user_id}/event/{event_id}/picks [N]
* /entry/{user_id}/history [Y]
* /entry/{user_id}/transfers [Y]
* /events [N]
* /event/{event_id}/live [Y]
* /fixtures/?event={event_id} [Y]
* /game-settings [N]
* /leagues-classic-standings/{league_id} [N]
* /leagues-classic-standings/{league_id} [N]
* /leagues-entries-and-h2h-matches/league/{league_id} [N]
* /leagues-h2h-standings/{league_id} [N]
* /my-team/{user_id}
* /teams
* /transfers

Element-stats Labels:
label: Minutes played
name: minutes
label: Goals scored
name: goals_scored
label: Assists
name: assists
label: Clean sheets
name: clean_sheets
label: Goals conceded
name: goals_conceded
label: Own goals
name: own_goals
label: Penalties saved
name: penalties_saved
label: Penalties missed
name: penalties_missed
label: Yellow cards
name: yellow_cards
label: Red cards
name: red_cards
label: Saves
name: saves
label: Bonus
name: bonus
label: Bonus Points System
name: bps
label: Influence
name: influence
label: Creativity
name: creativity
label: Threat
name: threat
label: ICT Index
name: ict_index
"""

coreApi = 'https://fantasy.premierleague.com/api/'
playerSummary = "element-summary/"
# User summary = summary of the  player where the number on the end is the player ID: https://fantasy.premierleague.com/api/element-summary/301/
classicStandings = "leagues-classic-standings/"
h2hStandings = "leagues-h2h-standings/"
teams = "entry/"
gameweekSummarySub = "bootstrap-static/"
playersInfoSub = "allPlayersInfo.json"
userInput = ""
playersFileName = "players"

# Quit the program if the user decides they want to leave
def endRoutine():
    print("// Would you like to run another function?")
    print("Y/N:")

    finalDecision = str.lower(input("> "))

    if "y" in finalDecision:
        print("------------------------------------------------------")
        print("")
        introRoutine()
    else:

        sys.exit()

# The first stage of the program. Contains the top menu items for the console app
def introRoutine():
    print("------------------------------------------------------------------------------")
    print("To access the different areas of the data type below what you want to see from:")
    print("!! PLEASE SELECT A NUMBER")
    print("------------------------------------------------------------------------------")
    print(" [1] Players")
    print(" [2] Teams")
    print(" [3] Game week summary")
    print(" [4] My league performance")
    print("")
    print(" [0] Experimental methods")
    print("------------------------------------------------------------------------------")
    print("")
    print("What would you like to see?:")
    userInput = input(">")
    print("")
    genericMethods.parse(userInput)
    if genericMethods.isInt(userInput) == True:
        userInputInt = int(userInput)
        if userInputInt ==  1:
            playerRoutine()
            
        if userInputInt == 2:
            teamsRoutine()

        if userInputInt ==  3:
            gameweekRoutine()

        if userInputInt == 0:
            # TODO: Remove this eventually before release
            experimentalRoutine()

        else:            
            print("====================================================================================")
            print("!! ERROR:Command not recognised - please pick one of the above options and try again:")
            print("====================================================================================")
            print("")
            introRoutine()

    elif userInput == "game week summary":
        gameweekSummary.printAllData(gameweekSummarySub, "playersSub")

    else:
        print("====================================================================================")
        print("!! ERROR:Input was not a number - please pick one of the above options and try again:")
        print("====================================================================================")
        print("")
        print("")
        introRoutine()

# Player specific section of the program. Contains the menu items for the player part of the console app
def playerRoutine():
    print("------------------------------------------------------------------------")
    print("You've said you want to take a look at the player data. You can look at:")
    print("!! PLEASE SELECT A NUMBER")
    print("------------------------------------------------------------------------")
    print(" Print to console:")
    print(" [1] Single player data for current gameweek (by surname)")
    print(" [2] Create predictions of performance for next gameweek")
    print(" [3] Create prediction constants for all player fields based on historical data from all seasons available")
    print(' [4] Top performers by position for last N gameweeks with gameweek difficulty (and next gameweek difficulty?)')
    print(' [5] Players by Influence')
    print(' [6] Players by Factor for teams')
    print(' [7] Players by Factors for whole game')
    print(' [8] Players ICT - print change over time')
    print(' [9] Top N players - Percentage played')
    print(' [10] Top involvement in goals')
    print(' [11] Differentials (Points per % Selected)')
    print(' [12] Consistency (Deviation from average for top N players)')
    print(' [13] Pick me a player')
    print(' [14] Pick me a captain')
    print(' [15] Pick me a transfer')
    print(' [16] Pick my team')
    print("")
    print(" Data Exports: ")
    print(" [51] All player data for all gameweeks (to excel)")
    print(" [52] All player data for all gameweeks for all years (to excel)")
    print("")
    print(" TEST:")
    print(" [99] Test: Rank player performance")
    print(" [100] Test: How previous performance affects future performance")
    print(" [101] Test: Get players details from detailed site")
    print("------------------------------------------------------------------------")
    print("")
    print("What would you like to see?:")
    playerUserInputInitial = input(">")
    print("")
    genericMethods.parse(playerUserInputInitial)

    if genericMethods.isInt(playerUserInputInitial) == True:
        playerUserInputInitialInt = int(playerUserInputInitial)

        #Single player data for current gameweek (by surname)
        if playerUserInputInitialInt == 1:
            print("-----------------------------------")
            print("Let us know who you're looking for:")
            print("!! TYPE IN A SURNAME")
            print("-----------------------------------")
            playerSurname = str.lower(input("> "))
            gameweekSummary.playerInfoBySurname(playerSurname)
            endRoutine()

        # Create predictions of performance for next gameweek
        elif playerUserInputInitialInt == 2:
            gameweekNumber = genericMethods.generateCurrentGameweek()
            currentGameweek = gameweekNumber - 6
            if currentGameweek < 0 :
                currentGameweek = 1
            correlationDictByWeek = dict()
            allGameweekData = dict()
            while currentGameweek <= gameweekNumber:
                progressStart = currentGameweek
                progressEnd = gameweekNumber
                print("")
                print("--------------------------------------------------")
                print(f"Data gathering: {progressStart} of {progressEnd}:")
                dataForCurrentGameweek = gameweekSummary.generateDataForGameWeek(currentGameweek)
                allDataForCurrentGameweek = playerData.convertStringDictToInt(dataForCurrentGameweek)
                allGameweekData[currentGameweek] = allDataForCurrentGameweek
                currentGameweek += 1
            print("--------------------------------------------------")
            print("")
            for gameweek in allGameweekData:   
                progressStart = gameweek - 1
                progressEnd = gameweekNumber - 1
                previousGameweek = gameweek - 1
                if previousGameweek > 0:
                    print("-----------------------------------------------")
                    print(f"Correlation: {progressStart} of {progressEnd}:")
                    playerPerformance = playerData.generateCorrelCoeffToPredictPerfomanceBasedOnPastWeek(allGameweekData, gameweek)
                    correlationDictByWeek[gameweek] = playerPerformance
                    print("-----------------------------------------------")

                        
            print("Correlations completed")
            print("")
            print("---------------------------------------------")
            print("")

            averageCorrelByField = genericMethods.convertCorrelByWeekToAveragePerField(correlationDictByWeek)

            previousWeek = gameweekNumber - 1
            predictionsForGameweek = playerData.playerPerformanceWithCorrel(previousWeek, averageCorrelByField)

            print("--------------------------------------------")
            print(f'Predicted top 15 performers for GW{gameweekNumber}:')
            print("")
            genericMethods.printDataClean(predictionsForGameweek, 15,"","")
            print("--------------------------------------------")
            print("")
                        
            endRoutine()

        # Create prediction constants for all player fields based on historical data from all seasons available
        elif playerUserInputInitialInt == 3:
            playersByPosition = playerData.generateHistoricalDataByPositionByPlayer()
            firstPlayerKey = list(playersByPosition[1].keys())[0]
            firstDateKey = list(playersByPosition[1][firstPlayerKey].keys())[0]
            keyList = list(playersByPosition[1][firstPlayerKey][firstDateKey].keys())
            attributeByPosition = dict()
            for position in playersByPosition:
                maxLen = len(playersByPosition[position])
                attributeDict = dict()
                for key in keyList:
                    attributeList = list()
                    for player in playersByPosition[position]:
                        currentIndex = list(playersByPosition[position]).index(player)
                        playerNumber = currentIndex + 1
                        genericMethods.runPercentage(maxLen, currentIndex,f"Running player {playerNumber} of {maxLen}", "All player data formatting now complete")
                        for season in playersByPosition[position][player]:
                            for attribute in playersByPosition[position][player][season]:
                                if attribute == key:
                                    attributeList.append(playersByPosition[position][player][season][attribute])

                    attributeDict[key] = attributeList
                attributeByPosition[position] = attributeDict
            
            for position in attributeByPosition:
                attributesForPosition = attributeByPosition[position]
                totalPointsCurrentPosition =  genericMethods.generateSingleEntryDictFromDict(attributesForPosition , 'total_points')
                correl = genericMethods.correlcoeffGenerationForPrediction(attributesForPosition, totalPointsCurrentPosition)
                currentRList = playerData.rValuesPerField(correl)
                print("")

            averageCorrelByField = genericMethods.convertCorrelByWeekToAveragePerField(correlationDictByWeek)

            previousWeek = gameweekNumber - 1
            predictionsForGameweek = playerData.playerPerformanceWithCorrel(previousWeek, averageCorrelByField)

            print("--------------------------------------------")
            print(f'Predicted top 15 performers for GW{gameweekNumber}:')
            print("")
            genericMethods.printDataClean(predictionsForGameweek, 15,"","")
            print("--------------------------------------------")
            print("")
                        
            endRoutine()

        # Print out the top 5 performers for the last N weeks 
        if playerUserInputInitialInt == 4:                        
            print("----------------------------------------------------------------------------------------------")
            print("How many gameweeks do you want to see?")
            print("")
            userInput = int(input("> "))
            print("-----------------------------------------------------------------------------------------------")                     
            print("What is the max player value you want to see?")
            print("")
            price = int(input("> "))
            print("-----------------------------------------------------------------------------------------------")
            print("Initialising method...")
            nowGameweek = genericMethods.generateCurrentGameweek()
            fromGameweek = nowGameweek - userInput
            count = fromGameweek
            currentGameweek = nowGameweek - userInput
            playerIDs = playerData.generatePlayersIdsList()
            playerNames = playerData.generatePlayerNameToIDMatching()
            playerIDsToNames = playerData.generatePlayerIDToSurnameMatching()
            positions = playerData.generatePositionReferenceIDAsKey()
            teamIDandPlayerID = Teams.teamIDsAsKeysAndPlayerIDsAsList()
            gameweekDifficultyByTeam = Teams.teamIDsAsKeysAndGameweekDifficultyAsList(fromGameweek, nowGameweek)
            sumOfPlayerScores = dict()
            allGameweekData = dict()
            gameweekList = list()

            while count <= nowGameweek:
                gameweekList.append(count)
                count += 1

            gameweekListClean = "/ "
            for week in gameweekList:
                gameweekListClean += f"{week} / "

            length = len(playerIDs) - 1
            for playerID in playerIDs:
                playerDataList = playerData.generateListOfPointsForNGameweeksPerPlayer(playerID, currentGameweek, nowGameweek, price, 'int')
                sumOfPlayerScores[playerID] = sum(playerDataList)
                allGameweekData[playerID] = playerDataList

                currentIndex = list(playerIDs).index(playerID)
                genericMethods.runPercentage(length, currentIndex, 'Gathering player scores', 'Player score data gathered')                           
                            
            sortedByPosition = playerData.sortPlayerDataByPosition(allGameweekData)
            sortedSumByPosition = playerData.sortPlayerDataByPosition(sumOfPlayerScores)


            playerNameTeamID = dict()

            for position in sortedByPosition:
                positionName = positions[position]
                currentPositionData = sortedByPosition[position]
                sortedSumPoints = sorted(sortedByPosition[position].items(), key=lambda x: sum(x[1]), reverse=True)
                top5Players = sortedSumPoints[:5]
                finalSumPoints = genericMethods.reformattedSortedTupleAsDict(top5Players)
                top5PlayersPreviousGameweeks = dict()

                for player in finalSumPoints:
                    for teamID in teamIDandPlayerID:
                        if player in teamIDandPlayerID[teamID]: 
                            playerNameTeamID[player] = teamID
                    playerName = playerNames[player].capitalize()
                    top5PlayersPreviousGameweeks[playerName] = currentPositionData[player]

                numberOfGames = userInput + 1

                print("-----------------------------------------------------------------------------------------------------------")
                print(f'Top ranked {positionName}s for points over the last {numberOfGames} games (GW {fromGameweek} to {nowGameweek}):')
                print("")
                print(f"Gameweek: {gameweekListClean}")
                print("")
                for player in top5PlayersPreviousGameweeks:
                    playerID = playerIDsToNames[str.lower(player)]
                    remainingLength = 15 - len(player)
                    gameDifficulty = "Game difficulty"
                    playerName = player + genericMethods.repeatStringToLength(" ", remainingLength) 
                    if remainingLength < 0 :
                        supplementLength = len(player) - 15
                        gameDifficulty = "Game difficulty" + genericMethods.repeatStringToLength(" ", supplementLength) 
                        playerName = player
                    teamID = playerNameTeamID[playerID]
                    difficultyList = str(gameweekDifficultyByTeam[teamID]).replace("[","").replace("]","")
                    playerDataTop5 = str(top5PlayersPreviousGameweeks[player]).replace("[","").replace("]","")
                    print(f"{playerName}: {playerDataTop5}")
                    print(f"{gameDifficulty}: {difficultyList}")
                    print("")
                print("-----------------------------------------------------------------------------------------------------------")
                print("")
            endRoutine()
                    
        if playerUserInputInitialInt == 5:
            currentGameweek = genericMethods.generateCurrentGameweek()
            print("Gathering player influence scores...")
            playersByInfluence = playerData.playerInfluence(currentGameweek)
            playerNames = playerData.generatePlayerNameToIDMatching()

            print("-----------------------------------------------------------------------------------------------------------")
            print(f'Top ranked players for points for GW{currentGameweek}:')
            print("")
            print("")
            for player in playersByInfluence:
                playerName = str(playerNames[player]).capitalize()
                playerInfluence = playersByInfluence[player]
                print(f"{playerName}: {playerInfluence}")

            endRoutine()

        # Top contributers to team influence
        if playerUserInputInitialInt == 6:
            gameweek = genericMethods.generateCurrentGameweek()
            currentGameweek = int(input(f"Which gameweek do you want to see data for (current gameweek = {gameweek}? > "))
            print("")
            n = int(input("How many players would you like to see? > "))
            playersByTeam = Teams.teamIDsAsKeysAndPlayerIDsAsList()
            factorByPlayer = playerData.playerPerformanceFactor(currentGameweek)
            factorByTeam = Teams.teamFactor(currentGameweek)
            playerNames = playerData.generatePlayerNameToIDMatching()
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            playerDict = dict()
            for team in teams:
                teamName = teams[team]
                teamFactor = sum(factorByTeam[team].values())
                for player in playersByTeam[team]:
                    try:
                        percentageFactor = (factorByPlayer[player]/teamFactor) * 100
                        playerName = playerNames[player].capitalize()
                        playerDict[playerName] = percentageFactor
                    except:
                        None
            playersSorted = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
            playersToPrint = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            topPlayers = {k: playersToPrint[k] for k in list(playersToPrint)[:n]}
            
            print(f"Top {n} Players that are most likely to be top performers for their team (% likelihood):")
            print("")
            for player in topPlayers:
                playerName = player.capitalize()
                playerInfluence = round(topPlayers[player],1)
                print(f"{playerName}: {playerInfluence}%")
            print("-----------------------------------")
            print("")

            endRoutine()

        # Top contributors to team performance
        if playerUserInputInitialInt == 7:
            gameweek = genericMethods.generateCurrentGameweek()
            currentGameweek = int(input(f"Which gameweek do you want to see data for (current gameweek = {gameweek}? > "))
            print("")
            n = int(input("How many players would you like to see? > "))
            playersByTeam = Teams.teamIDsAsKeysAndPlayerIDsAsList()
            factorByPlayer = playerData.playerPerformanceFactor(currentGameweek)
            factorByTeam = Teams.teamFactor(currentGameweek)
            playerNames = playerData.generatePlayerNameToIDMatching()
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            playerDict = dict()
            for team in teams:
                teamName = teams[team]
                allValues = sum(factorByPlayer.values())
                for player in playersByTeam[team]:
                    try:
                        percentageFactor = (factorByPlayer[player]/allValues) * 100
                        playerName = playerNames[player].capitalize()
                        playerDict[playerName] = percentageFactor
                    except:
                        None
            playersSorted = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
            playersToPrint = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            topPlayers = {k: playersToPrint[k] for k in list(playersToPrint)[:n]}
            
            print(f"Top {n} Players that are most likely to be top performers overall (% contribution to total league peformance next week):")
            print("")
            for player in topPlayers:
                playerName = player.capitalize()
                playerInfluence = round(topPlayers[player],1)
                print(f"{playerName}: {playerInfluence}%")
            print("-----------------------------------")
            print("")

            endRoutine()

        # Print ICT history to the console
        if playerUserInputInitialInt == 8:
            numberOfGameweeks = int(input("How many weeks would you like to see? > "))
            print(" 1. Vs. Gameweek Difficulty")
            print(" 2. Vs. Points scored")
            RouteToTake = int(input("What would you like to compare against? > "))
            currentGameweek = genericMethods.generateCurrentGameweek()
            count = currentGameweek + 1 - numberOfGameweeks
            playerList = playerData.generatePlayerNameToIDMatching() 
            gameweekList = list()

            while count <= currentGameweek:
                gameweekList.append(count)
                count += 1

            gameweekListHeaders = ['Name']
            for week in gameweekList:
                gameweekListHeaders.append(f'GW{week}')
            gameweekListHeaders.append('*AVG*')


            playerICTHistory = playerData.generateHistoryOfICTForNGameweeks(numberOfGameweeks - 1, RouteToTake)
            playerICTList = dict()
            playerComparativeList = dict()
            maxLen = len(playerICTHistory)
            for player in playerICTHistory:
                currentPlayerICTList = list()
                currentPlayerComparative = list()
                currentIndex = list(playerICTHistory.keys()).index(player)
                genericMethods.runPercentage(maxLen, currentIndex, "Generating players ICT shortlist", "Final shortlist of top ICT players created")
                for ICTHistory in playerICTHistory[player]:
                    currentPlayerICTList.append(playerICTHistory[player][ICTHistory][ICTHistory])
                    currentPlayerComparative.append(str(playerICTHistory[player][ICTHistory]['comparative']))
                
                playerICTList[player] = currentPlayerICTList
                playerComparativeList[player] = currentPlayerComparative

            averageICTByPlayer = dict()
            maxLen = len(playerICTList)
            for player in playerICTList:
                currentIndex = list(playerICTList.keys()).index(player)
                genericMethods.runPercentage(maxLen, currentIndex, "Generating Average ICT for player", "Average ICT for players created")
                averageICT = round(genericMethods.listAverage(playerICTList[player]),1)
                averageICTByPlayer[player] = averageICT 

            fromGameweek = currentGameweek - numberOfGameweeks

            sortedSumICT = sorted(averageICTByPlayer.items(), key=operator.itemgetter(1), reverse=True)
            top5Players = sortedSumICT[:5]
            finalSumICT = genericMethods.reformattedSortedTupleAsDict(top5Players)
            
            if RouteToTake == 1:
                comparative = "game difficulty"
            if RouteToTake == 2:
                comparative = "round points"

            totalICTPlayers = dict()
            topICTPlayers = dict()
            playerComparativeFinal = dict()
            for player in finalSumICT:
                playerComparativeListPrint = [f"{comparative.capitalize()}"]
                playerName = playerList[player].upper()
                averageComparative = genericMethods.listAverage(list(0 if x == '-' else int(x) for x in playerComparativeList[player]))
                if len(playerICTList[player]) < numberOfGameweeks:
                    numberOfZeros = numberOfGameweeks - len(playerICTList[player])
                    ICTUse = (["-"] * numberOfZeros) + playerICTList[player] + [averageICTByPlayer[player]]
                    playerComparativeList[player] = (['-'] * numberOfZeros) + playerComparativeList[player]
                    playerComparativeListPrint.extend(playerComparativeList[player])
                else:
                    ICTUse = playerICTList[player] + [averageICTByPlayer[player]]
                    playerComparativeListPrint.extend(playerComparativeList[player])
                formattedICT = [playerName]
                formattedICT.extend(ICTUse)
                topICTPlayers[player] = formattedICT
                playerComparativeFinal[player] = playerComparativeListPrint + [averageComparative]

            print("-----------------------------------------------------------------------------------------------------------")
            print(f'Top ranked players for ICT Index growth over the last {numberOfGameweeks} games (GW {fromGameweek + 1} to {currentGameweek}) compared to {comparative}:')
            print("")

            t = PrettyTable(gameweekListHeaders, hrules = prettytable.ALL)
            for player in topICTPlayers:
                t.add_row(topICTPlayers[player])
                t.add_row(playerComparativeFinal[player])
            print(t)
            print("")

            endRoutine()        

        # All players ordered by minutes played so far
        elif playerUserInputInitialInt == 9:
            n = int(input("How many players do you want to see? > "))
            percentageplayer = playerData.percentageTimePlayedByPlayer()
            sortedPercentagePlayed = sorted(percentageplayer.items(), key=operator.itemgetter(1), reverse=True)
            topNPlayers = sortedPercentagePlayed[:n]
            finalPlayers = genericMethods.reformattedSortedTupleAsDict(topNPlayers)
            print(f"Top {n} players for % of available time played")
            print("")
            for player in finalPlayers:
                value = finalPlayers[player]
                print(f"{player}: {value}%")

            endRoutine()

        
        # Top contributors to goals (% goal involvement)
        elif playerUserInputInitialInt == 10:
            n = int(input("How many players would you like to see? > "))
            teamGoals = Teams.totalTeamGoals()
            playerInvolvement = playerData.playerGoalInvolvement()
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            playerInfo = dict()
            playerDict = dict()
            for team in teams:
                teamName = teams[team]
                currentTeamGoals = teamGoals[team]
                playersInTeam = Teams.generateListOfPlayerIDsAsKeysForTeam(team)
                for player in playersInTeam:
                    playerList = list()
                    try:
                        involvement = float(round((playerInvolvement[player]['involvement'] / currentTeamGoals)*100 , 1))
                    except:
                        involvement = 0.0
                    playerName = playerInvolvement[player]['name']
                    playerList.append(playerName)
                    playerList.append(str(involvement)+"%")
                    playerList.append(teamGoals[team])
                    playerList.append(playerInvolvement[player]['goals'])
                    playerList.append(playerInvolvement[player]['assists'])
                    playerDict[playerName] = involvement
                    playerInfo[playerName] = playerList

            playersSorted = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
            playersToPrint = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            topPlayers = {k: playersToPrint[k] for k in list(playersToPrint)[:n]}
            
            print("")
            print("")
            print(f"Involvement - Top {n} Players by % involvement in total goals scored:")
            print("")
            t = PrettyTable(['Name', 'Involvement (%)', 'Team Goals', 'Goals', 'Assists'], hrules = prettytable.ALL)
            for player in topPlayers:
                t.add_row(playerInfo[player])
            print(t)
            print("")

            endRoutine()

        # Differentials - points per percentage selected
        elif playerUserInputInitialInt == 11:
            n = int(input("How many players would you like to see? > "))
            highestValue = int(input("What is the HIGHEST VALUE you want to include? > "))
            lowestValue = int(input("What is the LOWEST VALUE you want to include? > "))
            minPercentage = int(input("What is the LOWEST PERCENTAGE SELECTED you want to include? > "))
            #TODO: Make the time for this method representative
            playerDifferentials = playerData.pointsPerSelectedPercentage(minPercentage, highestValue, lowestValue)
            playerInfo = dict()
            playerDict = dict()
            length = len(playerDifferentials)
            for player in playerDifferentials:
                currentIndex = list(playerDifferentials.keys()).index(player)
                genericMethods.runPercentage(length, currentIndex, f"Picking top players by differential", f"Top {n} players under £{highestValue}M in value")
                playerList = list()
                playerName = playerDifferentials[player]['name']
                playerList.append(playerName)
                playerList.append(round(playerDifferentials[player]['pointsPerPercent'], 1))
                playerList.append(playerDifferentials[player]['points'])
                playerList.append(str(playerDifferentials[player]['selected'])+'%')
                playerList.append('£'+str(playerDifferentials[player]['value'])+'M')
                playerList.append(playerDifferentials[player]['goals'])
                playerList.append(playerDifferentials[player]['assists'])
                playerList.append(playerDifferentials[player]['bonus'])
                playerList.append(playerDifferentials[player]['ict'])
                playerList.append(str(round(playerDifferentials[player]['minutesPercentage'],1))+'%')
                playerList.append(playerDifferentials[player]['pointsPerGame'])
                playerDict[playerName] = playerDifferentials[player]['pointsPerPercent']
                playerInfo[playerName] = playerList

            playersSorted = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
            playersToPrint = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            topPlayers = {k: playersToPrint[k] for k in list(playersToPrint)[:n]}
            
            print("")
            print("")
            print(f"Differentials - Top {n} Players for points per percentage where at least {minPercentage}% of people selected them:")
            print("")
            t = PrettyTable(['Name', 'Points per percent selected', 'Points scored', '% Selected', f'Value £{lowestValue} to {highestValue}M', 'Goals scored', 'Assists', 'Bonus Points', 'ICT Index', 'Total game time played (%)', 'Points Per Game'], hrules = prettytable.ALL)
            for player in topPlayers:
                t.add_row(playerInfo[player])
            print(t)
            print("")

            endRoutine()

            

        # Consistency - players that have the highest AND most consistent performance
        elif playerUserInputInitialInt == 12:
            n = int(input("How many players would you like to see? > "))
            players = playerData.generatePlayerIDToSurnameMatching()
            playerInfo = dict()
            playerPoints = dict()
            playerReference = dict()
            length = len(players)
            x = int(input(f"How many do you want to include in the cohort of 'best players' (max = {length})? > "))
            for player in players:  
                currentIndex = list(players).index(player)
                genericMethods.runPercentage(length, currentIndex, f"Picking top {x} players by points", f"Top {x} Players by points have been gathered")
                currentGameweek = genericMethods.generateCurrentGameweek()
                playerPerformance = playerData.generateListOfPointsForNGameweeksPerPlayer(players[player], 1, currentGameweek, 100000, 'int')
                playerName = player.capitalize()
                playerPoints[playerName] = sum(playerPerformance)
                playerReference[playerName] = players[player]

            playersSorted = sorted(playerPoints.items(), key=lambda x: x[1], reverse=True)
            playersToPrint = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            topPlayers = {k: playersToPrint[k] for k in list(playersToPrint)[:x]}

            length = len(topPlayers)
            playerDeviation = dict()
            for player in topPlayers:  
                currentIndex = list(topPlayers).index(player)
                genericMethods.runPercentage(length, currentIndex, "Finding the top performers", "Top performers for consistency gathered")
                currentGameweek = genericMethods.generateCurrentGameweek()
                playerID = playerReference[player]
                playerPerformance = playerData.generateListOfPointsForNGameweeksPerPlayer(playerID, 1, currentGameweek, 100000, 'int')
                playerList = list()
                averagePerformance = genericMethods.listAverage(playerPerformance)
                playerDeviationList = list()
                for performance in playerPerformance:
                    if genericMethods.percentageDifferenceToAverage(performance, averagePerformance) >= 0:
                        playerDeviationList.append(genericMethods.percentageDifferenceToAverage(performance, averagePerformance))
                    else:
                        playerDeviationList.append(-genericMethods.percentageDifferenceToAverage(performance, averagePerformance))

                playerName = player.capitalize()
                playerList.append(playerName)
                playerInfo[playerName] = playerList
                deviation = round(genericMethods.listAverage(playerDeviationList)*100, 1)
                playerList.append(deviation)
                playerList.append(round(averagePerformance, 1))
                playerList.append(sum(playerPerformance))
                playerList.append(max(playerPerformance))
                playerList.append(min(playerPerformance))
                playerDeviation[playerName] = deviation

            playersSorted = sorted(playerDeviation.items(), key=lambda x: x[1], reverse=False)
            playersToPrint = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            topPlayers = {k: playersToPrint[k] for k in list(playersToPrint)[:n]}
            
            print("")
            print("")
            print(f"Consistency - Top {n} Players for consistency of scoring points for the top {x} performers:")
            print("")
            t = PrettyTable(['Name', '% deviation from average', 'Average', 'Total',  'Max', 'Min'], hrules = prettytable.ALL)
            for player in topPlayers:
                t.add_row(playerInfo[player])
            print(t)
            print("")

            endRoutine()


        # Pick me a player - players that have the highest AND most consistent performance
        elif playerUserInputInitialInt == 13:
            players = genericMethods.generateJSONDumpsReadable("https://fantasy.premierleague.com/api/bootstrap-static/")
            lastGameweek = genericMethods.generateCurrentGameweek()
            # Price
            print("---- PRICE ------")
            price  = float(input("How much money do you have to spend? >> "))
            print("")
            
            # Position
            print("")
            print("---- POSITION ------")
            print("[1] Goalkeeper")
            print("[2] Defender")
            print("[3] Midfielder")
            print("[4] Striker")
            position = int(input("What position are you interested in? (use the numbers above) >> "))
            print("")
            
            # Teams to Exclude
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            print("")
            print("---- TEAMS ------")
            for teamId in teams:
                team = teams[teamId].capitalize()
                print(f'[{teamId}] = {team}')
            teamsExclude = input("What TEAM IDS are you NOT interested in? (use the numbers above) >> ").split(",")
            teamsExcludeClean = []
            if teamsExclude[0] != '':
                for team in teamsExclude:
                    teamsExcludeClean.append(int(team))
                teamInclude = list()
                for teamId in teams:
                    if teamId not in teamsExcludeClean:
                        teamInclude.append(int(teamId))
            if teamsExclude[0] == "":
                teamInclude = list()
                for teamId in teams:
                    teamInclude.append(int(teamId))
            print("")

            print("")
            print("---- HISTORY ------")
            lookback  = float(input(f"How many weeks do you want to look back? (last full gameweek was GW{lastGameweek}) >> "))
            print("")

            # Filter the IDs
            positionFilter = playerData.filterBootstrapStaticResults('element_type', int(position), players['elements'], '=')
            teamFilter = playerData.filterBootstrapStaticResults('team', teamInclude, positionFilter, 'in')
            filteredData = playerData.filterBootstrapStaticResults('now_cost', int(price*10), teamFilter, '<=')
            playerIDs = list(filteredData.keys())

            # Set up factors
            overallFactors = {
                'Total minutes played': {
                    'elements': ['minutes'], 
                    'lowIsGood': 'n', 
                    'zeroIsNullOrNone': 'n'
                    },
                'Percentage Selected by (Higher input = Less selected)':{
                    'elements': ['selected_by_percent'], 
                    'lowIsGood': 'y', 
                    'zeroIsNullOrNone': 'y'
                    },
                'Total points scored':{
                    'elements': ['total_points'], 
                    'lowIsGood': 'n', 
                    'zeroIsNullOrNone': 'n'
                    },
                'Average points per game': {
                    'elements': ['points_per_game'], 
                    'lowIsGood': 'n', 
                    'zeroIsNullOrNone': 'n'
                    },
                'ICT index': {
                    'elements': ['ict_index'], 
                    'lowIsGood': 'n', 
                    'zeroIsNullOrNone': 'n'
                    },
                'Bonus points scored':{
                    'elements': ['bonus'], 
                    'lowIsGood': 'n', 
                    'zeroIsNullOrNone': 'n'
                    },
                # TODO: Get momentum in this
                # 'Momentum (i.e. are they getting better?)':[''],
                }      

            if position == 1:
                positionFactors = {
                    'Clean Sheets':{
                        'elements': ['clean_sheets'], 
                        'lowIsGood': 'n', 
                        'zeroIsNullOrNone': 'n'
                        },
                    'Penalties saved': {
                        'elements': ['penalties_saved'], 
                        'lowIsGood': 'n', 
                        'zeroIsNullOrNone': 'n'
                        }
                    }

            if position in [2,3]:
                positionFactors = {
                    'Clean Sheets':{
                        'elements': ['clean_sheets'], 
                        'lowIsGood': 'n', 
                        'zeroIsNullOrNone': 'n'
                        },
                    'Assists':{
                        'elements': ['assists'], 
                        'lowIsGood': 'n', 
                        'zeroIsNullOrNone': 'n'
                        },
                    'Goals':{
                        'elements': ['goals_scored'], 
                        'lowIsGood': 'n', 
                        'zeroIsNullOrNone': 'n'
                        },
                    'Set piece player': {
                        'elements': ["corners_and_indirect_freekicks_order", "direct_freekicks_order", "penalties_order"], 
                        'lowIsGood': 'y', 
                        'zeroIsNullOrNone': 'y'
                        }
                    }

            if position == 4:
                positionFactors = {
                    'Assists':{
                        'elements': ['assists'], 
                        'lowIsGood': 'n', 
                        'zeroIsNullOrNone': 'n'
                        },
                    'Goals':{
                        'elements': ['goals_scored'], 
                        'lowIsGood': 'n', 
                        'zeroIsNullOrNone': 'n'
                        },
                    'Set piece player': {
                        'elements': ["corners_and_indirect_freekicks_order", "direct_freekicks_order", "penalties_order"], 
                        'lowIsGood': 'y', 
                        'zeroIsNullOrNone': 'y'
                        }
                    }

            factorWeights = dict()
            print("")
            print("------ PERFORMANCE FACTORS -------")
            print("Ranked out of 10, where 10 is 'Incredibly important' and 0 is 'Don't include in the analysis' how important are the following?")

            for factor in overallFactors:
                currentFactor = float(input(f"{factor} >> "))
                while currentFactor > 10:
                    print("")
                    print("NUMBER NOT LESS THAN 10!")
                    print("")
                    currentFactor = float(input(f"{factor} >> "))
                for item in overallFactors[factor]['elements']:
                    currentFactorDict = dict()
                    currentFactorDict['weight'] = currentFactor / 10
                    currentFactorDict['lowIsGood'] = overallFactors[factor]['lowIsGood']
                    currentFactorDict['zeroIsNullOrNone'] = overallFactors[factor]['zeroIsNullOrNone']
                    factorWeights[item] = currentFactorDict

            for factor in positionFactors:
                currentFactor = float(input(f"{factor} >> "))
                while currentFactor > 10:
                    print("")
                    print("NUMBER NOT LESS THAN 10!")
                    print("")
                    currentFactor = float(input(f"{factor} >> "))
                for item in positionFactors[factor]['elements']:
                    currentFactorDict = dict()
                    currentFactorDict['weight'] = currentFactor / 10
                    currentFactorDict['lowIsGood'] = positionFactors[factor]['lowIsGood']
                    currentFactorDict['zeroIsNullOrNone'] = positionFactors[factor]['zeroIsNullOrNone']
                    factorWeights[item] = currentFactorDict

            
            print("")
            print("-----------------------------")
            print("")

            startGameweek = lastGameweek - lookback
            keys = factorWeights.keys()

            playersData = gameweekSummary.generateSumDataForGameWeekRange(startGameweek, lastGameweek, playerIDs, keys)
            allPlayerDataForMaxMin = genericMethods.allDataAllPlayersByElementIdForGameweekRange(startGameweek, lastGameweek)
            allDataForMaxMin = genericMethods.allDataAllPlayersByElementId()
            indexDict = dict()

            allData = dict()

            playerDataKeys = list(allPlayerDataForMaxMin.keys())
            bootstrapDataKeys = list(allDataForMaxMin.keys())
            for field in keys:
                if field in playerDataKeys:
                    allData[field] = allPlayerDataForMaxMin[field]
                else:
                   allData[field] = allDataForMaxMin[field]

            finalData = dict()
            for player in playersData:
                try:
                    playerDict = dict()
                    for field in keys:
                        if field in playerDataKeys:
                            value = playersData[player] 
                        else:
                            value = filteredData[player]
                        playerDict[field] = value[field]
                    finalData[player] = playerDict
                except:
                    None

            maxValues = playerData.calculateMaxNumberInArray(allData)
            minValues = playerData.calculateMinNumberInArray(allData)

            playerList = dict()
            
            for player in finalData:
                playerResults = dict()
                for element in finalData[player]:
                    if element in keys:
                        maxValue = maxValues[element]
                        minValue = minValues[element]
                        if factorWeights[element]['zeroIsNullOrNone'] == 'y' and minValue == 0.0:
                            minValue = 1.
                        factor = factorWeights[element]['weight']
                        data = genericMethods.parseFloat(finalData[player][element])
                        if factorWeights[element]['zeroIsNullOrNone'] == 'y' and data == 0.0:
                            index = 0.0
                        else:
                            index = genericMethods.indexValue(data, maxValue, minValue, factorWeights[element]['lowIsGood']) * factor
                        playerResults[element] = index

                finalResult = genericMethods.dictAverage(playerResults)
                playerList[player] = finalResult
            
            playersSorted = sorted(playerList.items(), key=lambda x: x[1], reverse=True)
            playersPrepared = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            playersReady = {k: playersPrepared[k] for k in list(playersPrepared)[:5]}
            
            playerNames = playerData.generatePlayerIDAsKeySurnameAsResult()
            print("")

            gameweekDifficultyByTeam = Teams.teamIDsAsKeysAndGameweekDifficultyAsList(startGameweek, lastGameweek)
            playerGameweekDifficulty = dict()
            playerStats = dict()

            for player in playersReady:
                currentPlayer = dict()
                teamIDs = playerData.generateIDAsKeyTeamIdAsValue()
                if player == 271:
                    print("")
                playerDifficulty = gameweekDifficultyByTeam[teamIDs[player]]
                listedGameweekDifficulty = Teams.upcomingGameDifficultyListed(lookback + 1, playerData.generateIDAsKeyTeamIdAsValue()[player])
                playerDataList = playerData.generateListOfPointsForNGameweeksPerPlayer(player, startGameweek, lastGameweek, price, 'string')
                points = list()
                points.append("Points")
                for item in playerDataList:
                    points.append(str(item))
                difficulty = list()
                difficulty.append("Difficulty")
                for item in playerDifficulty:
                    difficulty.append(str(item))
                currentPlayer['points'] = points
                currentPlayer['difficulty'] = difficulty
                currentPlayer['future_difficulty'] = listedGameweekDifficulty

                count = startGameweek
                gameweekList = list()
                gameweekList.append("Gameweek")
                playerGameweeksPlayed = playerData.gameweeksPlayed(player)
                weeksWeCareAbout = list()
                n = startGameweek
                maxReached = False
                while n <= lastGameweek:
                    weeksWeCareAbout.append(n)
                    n += 1
                previousGameweek = startGameweek
                for gameweek in playerGameweeksPlayed:
                    currentGameweek = gameweek
                    difference = currentGameweek - previousGameweek
                    if gameweek in weeksWeCareAbout:
                        if str(gameweek) in gameweekList:
                            gameweekList.append(f"{gameweek}+")
                        if difference == 2 and str(gameweek) not in gameweekList:
                            gameweekList.append(str(gameweek - 1))
                        if  str(gameweek) not in gameweekList:
                            gameweekList.append(str(gameweek))
                    previousGameweek = gameweek

                currentPlayer['pastGameweeks'] = gameweekList
                playerGameweekDifficulty[player] = currentPlayer


            futureGameweeks = list()
            futureGameweeks.append("Gameweek")
            count = lastGameweek + 1
            while count <= lastGameweek + (lookback + 1):
                futureGameweeks.append(int(count))
                count += 1
            

            for player in playersReady:
                rank = list(playersPrepared).index(player) + 1
                print("")
                print(f"---------- PLAYER RANKED NO. {rank} ----------")
                print("")
                gameweekSummary.playerInfoById(player, position)
                print("")
                print("/ Form Card:")
                print("")
                headers = playerGameweekDifficulty[player]['pastGameweeks']
                t = PrettyTable(headers, hrules = prettytable.ALL)
                points = playerGameweekDifficulty[player]['points']
                difficulty = playerGameweekDifficulty[player]['difficulty']
                t.add_row(difficulty)
                t.add_row(points)
                print(t)
                print("")
                print("/ Future gameweek difficulty:")
                print("")
                y = PrettyTable(futureGameweeks, hrules = prettytable.ALL)
                gameweeks = ['Difficulty']
                for difficulty in playerGameweekDifficulty[player]['future_difficulty']:
                    gameweeks.append(difficulty)
                y.add_row(gameweeks)
                print(y)
                print("---------------------------------------------------")
                print("")

            endRoutine()

        elif playerUserInputInitialInt == 14:
            gw = genericMethods.generateCurrentGameweek() + 1
            print("-----------------------------------------------------------------------------------------------------------")
            print(f'Which Gameweek do you want to see (next gameweek = {gw})?')
            print("-------------------------------------------------------")
            print("")
            gw = int(input("Gameweek >> "))
            easiestGames = Teams.gameweekDifficultyRankedForTeams(gw, 0)
            fixtureIndex = dict()
            for fixture in easiestGames:
                fixtureIndex[fixture] = int(round(genericMethods.indexValue(easiestGames[fixture],max(list(easiestGames.values())),min(list(easiestGames.values())),"n"), 0))
            top5FixtureTeams = list(fixtureIndex.keys())[:5]
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            top5Fixtures = dict()
            for fixture in top5FixtureTeams:
                top5Fixtures[teamNames[fixture]] = easiestGames[fixture]
            n = 3
            if gw - 3 <= 0:
                n = 2
            if gw - 2 <= 0:
                n = 1
            if gw - 1 <= 0:
                n = 0
            influenceByPlayer = playerData.playerInfluenceInAGivenTimeFrameByTeam(gw-1, n)
            influenceByTeam = Teams.teamInfluenceInAGivenTimeFrame(gw-1, n)
            playerNames = playerData.generatePlayerNameToIDMatching()
            playerNamesToId = playerData.generatePlayerIDToSurnameMatching()  
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            playerToTeam = playerData.generateIDAsKeyTeamIdAsValue()
            chanceOfPlaying = playerData.generateChanceOfPlaying()
            playerDumps = genericMethods.generateJSONDumpsReadable("https://fantasy.premierleague.com/api/bootstrap-static/")['elements']

            def captainRoutine(gw, influenceByTeam, influenceByPlayer,playerNamesToId, playerNames, teams, playerToTeam, chanceOfPlaying, playerDumps):
                
                myTeam = Teams.getMyTeam(gw)

                potentialCaptains = list()
                playerPerformance = dict()

                for player in myTeam['picks']:
                    performance = list()
                    if playerToTeam[player['element']] in list(top5Fixtures.keys()):
                        potentialCaptains.append(str(playerNames[player['element']]).capitalize())
                        n = gw - 3
                        if n <= 0:
                            n = 1
                        while n < gw:
                            playerHistory = playerData.generateListOfPlayersAndMetricsRelatedToPerformance(player['element'], n)
                            if len(list(playerHistory.values())) == 0:
                                playerHistory = playerData.generateListOfPlayersAndMetricsRelatedToPerformance(player['element'], n - 3)
                                totalPoints = playerHistory['total_points']
                                performance.append(totalPoints)
                            else:
                                totalPoints = playerHistory['total_points']
                                expectedPlay = playerHistory
                                performance.append(totalPoints)
                            n += 1

                        playerPerformance[str(playerNames[player['element']]).capitalize()] = sum(performance)

                expectedCaptains = dict()

                chanceConverter = {100:100, 75:50, 50:25, 25:0, 0:0}

                for player in playerPerformance:
                    playerID = playerNamesToId[player.lower()]
                    teamInfluence = influenceByTeam[playerToTeam[playerID ]]
                    playerInfluence = influenceByPlayer[playerToTeam[playerID]][playerID ]
                    influenceFactor = playerInfluence/teamInfluence
                    playerChanceOfPlaying = chanceConverter[chanceOfPlaying[playerID]]/100
                    expectedPerformance = ((playerPerformance[player] * fixtureIndex[teams[playerToTeam[playerID]]]) * influenceFactor) * playerChanceOfPlaying
                    expectedCaptains[player.capitalize()] = int(expectedPerformance)
                    captainsSorted = sorted(expectedCaptains.items(), key=lambda x: x[1], reverse=True)
                    captainsPrepared = genericMethods.reformattedSortedTupleAsDict(captainsSorted)
                
                print("Top captain picks:")

                n = 1
                for captain in captainsPrepared:
                    print(f'{n}. {captain}: {captainsPrepared[captain]}')
                    n += 1

            captainRoutine(gw, influenceByTeam, influenceByPlayer,playerNamesToId, playerNames, teams, playerToTeam, chanceOfPlaying, playerDumps)

            goAgain = str(input("Would you like to run another team? (Y/N) > ")).lower()
            
            if goAgain == 'y':
                captainRoutine(gw, influenceByTeam, influenceByPlayer,playerNamesToId, playerNames, teams, playerToTeam, chanceOfPlaying, playerDumps)

            endRoutine()
            
        elif playerUserInputInitialInt == 15:
            gw = genericMethods.generateCurrentGameweek() + 1
            print("-----------------------------------------------------------------------------------------------------------")
            print(f'Which Gameweek do you want to see (next gameweek = {gw})?')
            print("-------------------------------------------------------")
            print("")
            gw = int(input("Gameweek >> "))
            easiestGames = Teams.gameweekDifficultyRankedForTeams(gw, 5)
            fixtureIndex = dict()
            for fixture in easiestGames:
                fixtureIndex[fixture] = int(round(genericMethods.indexValue(easiestGames[fixture],max(list(easiestGames.values())),min(list(easiestGames.values())),"n"), 0))
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            influenceByPlayer = playerData.playerInfluenceInAGivenTimeFrameByTeam(gw-1, 5)
            influenceByTeam = Teams.teamInfluenceInAGivenTimeFrame(gw-1, 5)
            playerNames = playerData.generatePlayerNameToIDMatching()
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            playerToTeam = playerData.generateIDAsKeyTeamIdAsValue()
            chanceOfPlaying = playerData.generateChanceOfPlaying()
            playerDumps = genericMethods.generateJSONDumpsReadable("https://fantasy.premierleague.com/api/bootstrap-static/")['elements']

            chanceConverter = {100:100, 75:50, 50:25, 25:0, 0:0}

            playersPerformance = dict()
            playerPerformance = dict()

            length = len(playerNames) - 1
            for player in playerNames:
                currentIndex = list(playerNames).index(player)
                genericMethods.runPercentage(length,currentIndex,f"Running player {currentIndex} of {length}", "All player data has been collected")
                performance = list()
                n = gw - 3
                while n < gw:
                    playerHistory = playerData.generateListOfPlayersAndMetricsRelatedToPerformance(player, n)
                    if len(list(playerHistory.values())) == 0 and n > 3:
                        playerHistory = playerData.generateListOfPlayersAndMetricsRelatedToPerformance(player, n - 3)
                        if len(list(playerHistory.values())) > 0:
                            totalPoints = playerHistory['total_points']
                            performance.append(totalPoints)
                        else:
                            totalPoints = 0
                    else:
                        if 'total_points' in playerHistory: 
                            totalPoints = playerHistory['total_points']
                        else:
                            totalPoints = 0
                        expectedPlay = playerHistory
                        performance.append(totalPoints)

                    n += 1
                playerPerformance[player] = sum(performance)

                teamInfluence = influenceByTeam[playerToTeam[player]]
                playerInfluence = influenceByPlayer[playerToTeam[player]][player]
                if playerInfluence == 0 or teamInfluence == 0:
                    influenceFactor = 0
                else:
                    influenceFactor = playerInfluence/teamInfluence
                playerChanceOfPlaying = chanceConverter[chanceOfPlaying[player]]/100
                expectedPerformance = ((playerPerformance[player] * fixtureIndex[teams[playerToTeam[player]]]) * influenceFactor) * playerChanceOfPlaying
                playersPerformance[player] = int(expectedPerformance)

            
            playersSorted = sorted(playersPerformance.items(), key=lambda x: x[1], reverse=True)
            playersPrepared = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            
            # Sort the world players by position
            playersByPosition = playerData.sortPlayerDataByPosition(playersPrepared)

            # Gather my players and sort by position
            teamPerformance = dict()
            elements = list()
            myTeamSource = Teams.getMyTeam(gw)
            myTeam = myTeamSource['picks']
            for elementSummary in myTeam:
                player = elementSummary['element']
                elements.append(player)
                teamPerformance[player] = playersPrepared[player]
            myTeamSortedByPosition = playerData.sortPlayerDataByPosition(teamPerformance)

            myPlayersSorted = dict()
            for position in myTeamSortedByPosition:
                myPlayersSorted[position] = genericMethods.reformattedSortedTupleAsDict(sorted(myTeamSortedByPosition[position].items(), key=lambda x: x[1], reverse=True))
            
            playerPrices = playerData.generateListOfPlayersPrices()

            # Worst per position
            worst = dict()

            worst[1] = {"id": list(myPlayersSorted[1].keys())[-1], "score": myPlayersSorted[1][list(myPlayersSorted[1].keys())[-1]], "value": playerPrices[list(myPlayersSorted[1].keys())[-1]]}
            worst[2] = {"id": list(myPlayersSorted[2].keys())[-1], "score": myPlayersSorted[2][list(myPlayersSorted[2].keys())[-1]], "value": playerPrices[list(myPlayersSorted[2].keys())[-1]]}
            worst[3] = {"id": list(myPlayersSorted[3].keys())[-1], "score": myPlayersSorted[3][list(myPlayersSorted[3].keys())[-1]], "value": playerPrices[list(myPlayersSorted[3].keys())[-1]]}
            worst[4] = {"id": list(myPlayersSorted[4].keys())[-1], "score": myPlayersSorted[4][list(myPlayersSorted[4].keys())[-1]], "value": playerPrices[list(myPlayersSorted[4].keys())[-1]]}

            # Work out which of the same price I should transfer in

            playerPrices = playerData.generateListOfPlayersByPositionByCost()
            filteredPriceByPosition = dict()

            try:
                bank = myTeamSource['transfers']['bank']
            except:
                try:
                    bank = myTeamSource['entry_history']['bank']
                except:
                    bank = 0

            
            playerReference = dict()
            playerDifference = dict()
            for position in playerPrices:
                for player in playerPrices[position]:
                    availableMoney = worst[position]['value'] + bank
                    if playerPrices[position][player] <= availableMoney and playersPrepared[player] - worst[position]['score'] > 0 and player not in elements :
                        playerDifference[player] = {"id": player, "difference": playersPrepared[player] - worst[position]['score'], "position": position}
                        playerReference[player] = playersPrepared[player] - worst[position]['score']

            playersSorted = sorted(playerReference.items(), key=lambda x: x[1], reverse=True)
            playersReady = genericMethods.reformattedSortedTupleAsDict(playersSorted)

            top5Transfers = list(playersReady.keys())[:5]

            positionRef = list()
            topByPosition = list()

            for player in playersReady:
                if playerDifference[player]['position'] not in positionRef:
                    topByPosition.append(player)
                    positionRef.append(playerDifference[player]['position'])
                if len(positionRef) == 4:
                    break

            positionRef = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}

            print("")
            print(" ----- TOP 5 TRANSFERS ------")
            print("")
            n = 1
            for player in top5Transfers:
                position = playerDifference[player]['position']
                playerOut = playerNames[worst[position]['id']]
                playerName = playerNames[player]
                playerValue = playerDifference[player]["difference"]
                print(f"{n}. {playerOut} out for {playerName} - {playerValue}")
                n += 1
            print("")

            print("")
            print(" ----- TOP TRANSFERS PER POSITION------")
            print("")
            n = 1
            for player in topByPosition:
                positionName = positionRef[playerDifference[player]['position']]
                position = playerDifference[player]['position']
                playerOut = playerNames[worst[position]['id']]
                playerName = playerNames[player]
                playerValue = playerDifference[player]["difference"]
                print(f"{positionName}: {playerOut} out for {playerName} - {playerValue}")
                n += 1
            print("")

            endRoutine()        

        elif playerUserInputInitialInt == 16:
            firstRun = True
            gw = genericMethods.generateCurrentGameweek() + 1
            print("-----------------------------------------------------------------------------------------------------------")
            print(f'Which Gameweek do you want to see (next gameweek = {gw})?')
            print("-------------------------------------------------------")
            print("")
            gw = int(input("Gameweek >> "))
            easiestGames = Teams.gameweekDifficultyRankedForTeams(gw, 5)
            fixtureIndex = dict()
            for fixture in easiestGames:
                fixtureIndex[fixture] = int(round(genericMethods.indexValue(easiestGames[fixture],max(list(easiestGames.values())),min(list(easiestGames.values())),"n"), 0))
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            influenceByPlayer = playerData.playerInfluenceInAGivenTimeFrameByTeam(gw-1, 5)
            influenceByTeam = Teams.teamInfluenceInAGivenTimeFrame(gw-1, 5)
            playerNames = playerData.generatePlayerNameToIDMatching()
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            playerToTeam = playerData.generateIDAsKeyTeamIdAsValue()
            chanceOfPlaying = playerData.generateChanceOfPlaying()
            playerDumps = genericMethods.generateJSONDumpsReadable("https://fantasy.premierleague.com/api/bootstrap-static/")['elements']

            chanceConverter = {100:100, 75:50, 50:25, 25:0, 0:0}

            playersPerformance = dict()
            playerPerformance = dict()

            length = len(playerNames) - 1
            for player in playerNames:
                currentIndex = list(playerNames).index(player)
                genericMethods.runPercentage(length,currentIndex,f"Running player {currentIndex} of {length}", "All player data has been collected")
                performance = list()
                n = gw - 3
                while n < gw:
                    playerHistory = playerData.generateListOfPlayersAndMetricsRelatedToPerformance(player, n)
                    if len(list(playerHistory.values())) == 0 and n > 3:
                        playerHistory = playerData.generateListOfPlayersAndMetricsRelatedToPerformance(player, n - 3)
                        if len(list(playerHistory.values())) > 0:
                            totalPoints = playerHistory['total_points']
                            performance.append(totalPoints)
                        else:
                            totalPoints = 0
                    else:
                        if 'total_points' in playerHistory: 
                            totalPoints = playerHistory['total_points']
                        else:
                            totalPoints = 0
                        expectedPlay = playerHistory
                        performance.append(totalPoints)

                    n += 1
                playerPerformance[player] = sum(performance)

                teamInfluence = influenceByTeam[playerToTeam[player]]
                playerInfluence = influenceByPlayer[playerToTeam[player]][player]
                if playerInfluence == 0 or teamInfluence == 0:
                    influenceFactor = 0
                else:
                    influenceFactor = playerInfluence/teamInfluence
                playerChanceOfPlaying = chanceConverter[chanceOfPlaying[player]]/100
                expectedPerformance = ((playerPerformance[player] * fixtureIndex[teams[playerToTeam[player]]]) * influenceFactor) * playerChanceOfPlaying
                playersPerformance[player] = int(expectedPerformance)

            
            playersSorted = sorted(playersPerformance.items(), key=lambda x: x[1], reverse=True)
            playersPrepared = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            
            # Sort the world players by position
            playersByPosition = playerData.sortPlayerDataByPosition(playersPrepared)

            # Gather my players and sort by position
            def teamPicker(playersPrepared, playersByPosition):
                teamPerformance = dict()
                elements = list()
                finalPlayerDict = dict()
                myTeamSource = Teams.getMyTeam(gw)
                myTeam = myTeamSource['picks']
                for elementSummary in myTeam:
                    player = elementSummary['element']
                    elements.append(player)
                    teamPerformance[player] = playersPrepared[player]
                myTeamBestToWorst = genericMethods.reformattedSortedTupleAsDict(sorted(teamPerformance.items(), key=lambda x: x[1], reverse=True))
                listToOrder = list(myTeamBestToWorst)[:11]
                for player in listToOrder:
                    finalPlayerDict[player] = myTeamBestToWorst[player]
                myTeamSortedByPosition = playerData.sortPlayerDataByPosition(finalPlayerDict)

                myPlayersSorted = dict()
                for position in myTeamSortedByPosition:
                    myPlayersSorted[position] = genericMethods.reformattedSortedTupleAsDict(sorted(myTeamSortedByPosition[position].items(), key=lambda x: x[1], reverse=True))
            
                positionRef = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}
                positionMaxMin = {1: {"max":1,"min":1}, 2: {"max":5,"min":3}, 3: {"max":5,"min":2}, 4: {"max":3,"min":1}}

                # TODO - Number of required players by position, sort all players too
                print("")
                print("")
                for position in myPlayersSorted:
                    positionName = positionRef[position]
                    print(f"====== Position: {positionName}: ======")
                    positionMax = positionMaxMin[position]["max"]
                    positionMin = positionMaxMin[position]["min"]
                    n = 1
                    for player in myPlayersSorted[position]:
                        if n <= positionMax:
                            playerName = playerNames[player]
                            playerValue = myPlayersSorted[position][player]
                            print(f"{playerName} = {playerValue}")
                            n += 1
                        else:
                            break
                    print(f"=======================================")
                    print("")
                print("")

                print(" All players sorted:")
                for player in myTeamBestToWorst:
                        playerName = playerNames[player]
                        playerValue = myTeamBestToWorst[player]
                        print(f"{playerName} = {playerValue}")

            if firstRun == True:
                teamPicker(playersPrepared, playersByPosition)
                firstRun = False
            goAgain = input("Do you want to run another team? (Y/N) > ")
            while goAgain in ["Y","y"]:
                teamPicker(playersPrepared, playersByPosition)
            endRoutine()        


        # All player data for all gameweeks (to excel)
        elif playerUserInputInitialInt == 51:
            playerIDs = gameweekSummary.generatePlayerIDs()
            playerData.exportPlayerDataByGameweek(playerIDs)
                        
            endRoutine()        
            
        # All player data for all gameweeks for all years (to excel)
        elif playerUserInputInitialInt == 52:
            playerIDs = gameweekSummary.generatePlayerIDs()
            allDataByYear = playerData.generateAllDataForAllYears(playerIDs)
            playerData.exportDictionaryOfDataToExcel(allDataByYear)
                        
            endRoutine()
                                   
        elif playerUserInputInitialInt == 99:
            gameweekNumber = genericMethods.generateCurrentGameweek()
            previousWeek = gameweekNumber - 1
            # TODO: Fix this method
            playerPerformance = playerData.playerPerformanceForLastWeek(previousWeek)
            print("")
            print("-----------------------------------")
            print("Would you like to export the data?:")
            print("!! TYPE IN Y/N")
            print("-----------------------------------")
            userInput = str.lower(input("> "))
            if userInput == 'y':
                gameweekHeaders = generateCommaSeperatedGameweekNumberList()
                genericMethods.printListToExcel(playerPerformance, gameweekHeaders)
            else:
                endRoutine()

        elif playerUserInputInitialInt == 100:
            gameweekNumber = genericMethods.generateCurrentGameweek()
            print("---------------------------------------------------------------")
            print("Let us know what week you're interested in:")
            print(f"!! TYPE IN A GAMEWEEK NUMBER (CURRENT GAMEWEEK NO. IS: {gameweekNumber})")
            print("---------------------------------------------------------------")
            gameweekNumber = str.lower(input("> "))
            if gameweekNumber == "now":
                gameweekNumber = genericMethods.generateCurrentGameweek()
                previousGameWeek = genericMethods.generateCurrentGameweek() - 1
            else:
                previousGameWeek = int(gameweekNumber) - 1
                gameweekNumber = int(gameweekNumber)
            playerPerformance = playerData.predictPlayerPerformanceByGameweek(gameweekNumber, previousGameWeek)
            formattedPlayerPerformance = genericMethods.listToDict(playerPerformance)
            print("")
            print("-----------------------------------")
            print("Would you like to export the data?:")
            print("!! TYPE IN Y/N")
            print("-----------------------------------")
            userInput = str.lower(input("> "))
            if userInput == 'y':
                headersOfData = generateHeadersList()
                genericMethods.printListToExcel(formattedPlayerPerformance, gameweekHeaders)
            else:
                endRoutine()             
                
        elif playerUserInputInitialInt == 101:
            playerList = detailedStats.getAllPlayers()
            players = detailedStats.getPlayerStats(playerList)
            players = detailedStats.getPlayerStatsDetailed(playerList)
            print()


        else:
            print("====================================================================================")
            print("!! ERROR:Command not recognised - please pick one of the above options and try again:")
            print("====================================================================================")
            print("")
            playerRoutine()

    else:
        print("====================================================================================")
        print("!! ERROR:Input was not a number - please pick one of the above options and try again:")
        print("====================================================================================")
        print("")
        playerRoutine()

# Teams specific section of the program. Contains the menu items for the teams part of the app
def teamsRoutine():
    print("------------------------------------------------------------------------")
    print("You've said you want to take a look at the teams data. You can look at:")
    print("!! PLEASE SELECT A NUMBER")
    print("------------------------------------------------------------------------")
    print(" Print to console:")
    print(" [1] Top N influencers (not those influencers)")
    print(" [2] Percentage influence of each player by team (messy maybe pick top 5 performers)")
    print(" [3] Net attack and defence for each team for next gameweek")
    print(" [4] Performance stats for a gameweek for a given team (TODO: add stats for players that week too)")
    print(" [5] Login and see top teams picks league")
    print(" [6] Average cost of position by team")
    print(" [7] Average game difficulty for the next N games ranked for all teams")
    print(" [8] Top 5 players by position for points per pound")
    print(" [9] Top performers by position for last N gameweeks")
    print(" [10] Fixture ranks by team - which teams have the easiest week")
    print(" [11] Goal economy by team")
    print("")
    print(" Goal and Result predictions")
    print("")
    print(" [12] Average goals conceded by team for difficulty this week")
    print(" [13] Average goals scored by team for difficulty this week")
    print(" [14] Predicting next gameweek results")
    print(" [15] Predicting next gameweek results based on goals")
    print(" [16] Weighted predictions for next gameweek based on goals")
    print("")
    print(" Historical Results: ")
    print("")
    print(" [17] Results by gameweek")
    print(" [18] Predictions for historical gameweeks")
    print(" [19] Predictions for historical gameweeks based on goals")
    print(" [20] Weighted predictions for historical gameweeks based on goals")
    print("")
    print("------------------------------------------------------------------------")
    print("")
    print(" [99] Weighted predictions for historical gameweeks based on goals - Outliers Removed")
    print(" [100] Weighted predictions for historical gameweeks based on goals - Outliers and Inliers weighted (70% and 30% respectively)")
    print("")
    print("What would you like to see?:")
    playerUserInputInitial = input(">")
    print("")
    genericMethods.parse(playerUserInputInitial)

    if genericMethods.isInt(playerUserInputInitial) == True:
        playerUserInputInitialInt = int(playerUserInputInitial)

        if playerUserInputInitialInt == 1:
            n = int(input("How many players would you like to see? > "))
            currentGameweek = genericMethods.generateCurrentGameweek()
            playersByTeam = Teams.teamIDsAsKeysAndPlayerIDsAsList()
            influenceByPlayer = playerData.playerInfluence(currentGameweek)
            influenceByTeam = Teams.teamInfluence(currentGameweek)
            playerNames = playerData.generatePlayerNameToIDMatching()
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            playerDict = dict()
            for team in teams:
                teamName = teams[team]
                teamInfluence = sum(influenceByTeam[team].values())
                for player in playersByTeam[team]:
                    try:
                        percentageInfluence = (influenceByPlayer[player]/teamInfluence) * 100
                        playerName = playerNames[player].capitalize()
                        playerDict[playerName] = percentageInfluence
                    except:
                        None
            playersSorted = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
            playersToPrint = genericMethods.reformattedSortedTupleAsDict(playersSorted)
            topPlayers = {k: playersToPrint[k] for k in list(playersToPrint)[:n]}

            print(f"Top {n} Players that are most likely to influence team performance (% contribution to team success):")
            print("")
            for player in topPlayers:
                playerName = player.capitalize()
                playerInfluence = round(topPlayers[player],1)
                print(f"{playerName}: {playerInfluence}%")
            print("-----------------------------------")
            print("")

            endRoutine()

        if playerUserInputInitialInt == 2:
            currentGameweek = genericMethods.generateCurrentGameweek()
            playersByTeam = Teams.teamIDsAsKeysAndPlayerIDsAsList()
            influenceByPlayer = playerData.playerInfluence(currentGameweek)
            influenceByTeam = Teams.teamInfluence(currentGameweek)
            playerNames = playerData.generatePlayerNameToIDMatching()
            teams = Teams.teamIDsAsKeysAndNamesAsData()
            teamDict = dict()
            for team in teams:
                teamName = teams[team]
                teamInfluence = sum(influenceByTeam[team].values())
                playerDict = dict()
                for player in playersByTeam[team]:
                    try:
                        percentageInfluence = (influenceByPlayer[player]/teamInfluence) * 100
                        playerName = playerNames[player].capitalize()
                        playerDict[playerName] = percentageInfluence
                    except:
                        None
                playersSorted = sorted(playerDict.items(), key=lambda x: x[1], reverse=True)
                playersToPrint = genericMethods.reformattedSortedTupleAsDict(playersSorted)
                teamDict[teamName] = playersToPrint

            for team in teamDict:
                teamName = team.capitalize()
                print(f"{teamName} players by influence:")
                print("")
                for player in teamDict[team]:
                    playerName = player.capitalize()
                    playerInfluence = round(teamDict[team][player],1)
                    print(f"{playerName}: {playerInfluence}%")
                print("-----------------------------------")
                print("")

            endRoutine()

        if playerUserInputInitialInt == 3:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1
            fixtures = Teams.fixturesForGameweekByTeamID(nextGameweek)
            strengthByTeam = Teams.strengthHomeAndAwayByTeam()
            teamNames = Teams.teamIDsAsKeysAndNamesAsData()
            print(f"Difference in team strengths for week {nextGameweek} fixtures")
            print("")
            for homeTeam in fixtures:
                awayTeam = fixtures[homeTeam]
                homeName = teamNames[homeTeam].capitalize()
                awayName = teamNames[awayTeam].capitalize()
                homeStandard = strengthByTeam[homeTeam]['homeOverall']
                homeOverall = strengthByTeam[homeTeam]['homeAttack'] - strengthByTeam[awayTeam]['awayDefence']
                awayStandard = strengthByTeam[awayTeam]['awayOverall']
                awayOverall = strengthByTeam[homeTeam]['homeDefence'] - strengthByTeam[awayTeam]['awayAttack']
                flatNetPerformance = homeOverall - awayOverall
                homePerformance = flatNetPerformance/homeStandard
                awayPerformance = (flatNetPerformance*-1)/awayStandard
                netPerformance = round(((homePerformance - awayPerformance) * 100) , 1)
                if netPerformance > 0:
                    print(f"{homeName} outperforms {awayName} by {netPerformance}%")
                elif netPerformance < 0 :
                    netPerformance = netPerformance * -1
                    print(f"{awayName} outperforms {homeName} by {netPerformance}%")
                else:
                    print(f"{awayName} and {homeName} are equally matched")

            endRoutine()
                

        if playerUserInputInitialInt == 4:
            print("-----------------------------------")
            print("Please type the team name in that you want to see data for:")
            print("")
            userInput = str.lower(input("> "))
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            teamID = teamNames[userInput]
            statsForPreviousGameweek = Teams.generateGameweekStats(teamID)  
            endRoutine()

        if playerUserInputInitialInt == 5:
            teamCap = int(input("How many teams do you want to pull data for?: "))
            print("-----------------------------------")
            print("Please log into your account to access league data:")
            print("")
            username = input("Email: ")
            password = input("Password: ")
            print(f'Gathering top {teamCap} teams data...')
            teamIDs = Teams.generateTeamIdsForTopPlayers(teamCap, username, password)
            playersSelectedCount = dict()
            print(f'Running through teams to capture top picked players...')
            # TODO: Turn into actual method and give progress
            for teamName in teamIDs:
                id = teamIDs[teamName]
                session = requests.session()
                currentTeamData = Teams.getTeamDetails(id, username, password, genericMethods.generateCurrentGameweek(), 'N')
                dataOfInterest = currentTeamData['picks']
                for data in dataOfInterest:
                    if data['element'] in playersSelectedCount:
                        playersSelectedCount[data['element']] += 1
                    else:
                        playersSelectedCount[data['element']] = 1
            referenceList = playerData.generatePlayerNameToIDMatching()
            playersMostSelected = dict()
            for id in playersSelectedCount:
                playerName = referenceList[id].capitalize()
                currentSelectedCount = playersSelectedCount[id]
                percentageSelected = int((playersSelectedCount[id] / teamCap) * 100)
                playersMostSelected[playerName] = percentageSelected

            playersSorted = sorted(playersMostSelected.items(), key=lambda x: x[1], reverse=True)
            finalPlayers = genericMethods.reformattedSortedTupleAsDict(playersSorted)
                        
            currentGameweek = genericMethods.generateCurrentGameweek()
            print("--------------------------------------------")
            print(f'Top 15 players picked by best performers for GW{currentGameweek}:')
            print("")
            genericMethods.printDataClean(finalPlayers, 15, '', '%')
            print("--------------------------------------------")

            endRoutine()

        if playerUserInputInitialInt == 6:
            print("-----------------------------------")
            print("Please type the position you're interested in:")
            print("(Goalkeeper, Defender, Midfielder, or Forward)")
            print("")
            userInput = str.lower(input("> "))
            positions = playerData.generatePositionReference()
            positionOfInterest = positions[userInput]
            positionName = userInput.capitalize()
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            positionAverageCost = dict()
            for currentTeam in teamNames:
                teamID = teamNames[currentTeam]
                team = currentTeam.capitalize()
                price = genericMethods.listAverage(playerData.generateListOfPlayersPricesInTeamByPosition(positionOfInterest, teamID))/10
                points = genericMethods.listAverage(playerData.generateListOfPlayersPointsInTeamByPosition(positionOfInterest, teamID))
                pricePerPoint = price/points
                positionAverageCost[team] = round(pricePerPoint, 2)

            sortedAverageCost = sorted(positionAverageCost.items(), key=lambda x: x[1], reverse=False)
            finalAverageCost = genericMethods.reformattedSortedTupleAsDict(sortedAverageCost)

            print("----------------------------------------------------------")
            print(f'Average cost per point of {positionName}s by team:')
            print("")
            genericMethods.printDataClean(finalAverageCost, 20, '£', 'M per point scored')
            print("----------------------------------------------------------")
            print("")

            endRoutine()

        if playerUserInputInitialInt == 7:
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            print("-----------------------------------")
            print("How many weeks do you want the average to be based off?:")
            print("")
            weekNumber = int(input("> "))
            listedDifficultyByTeam = dict()
            averageDifficultyByTeam = dict()
            finalDifficultyDict = dict()
            length = len(teamNames)-1

            for team in teamNames:
                currentIndex = list(teamNames).index(team)
                genericMethods.runPercentage(length, currentIndex, "Gathering list of upcoming game difficulty", "Complete: Calculating average game difficulty")

                currentTeamID = teamNames[team]
                listedGameweekDifficulty = list(map(lambda x:6 if x=="-" else x,Teams.upcomingGameDifficultyListed(weekNumber, currentTeamID)))
                readableTeamName = team.capitalize()
                listedDifficultyByTeam[readableTeamName] = listedGameweekDifficulty
                            
            gameweekList = list()
            count = genericMethods.generateCurrentGameweek() + 1
            nowGameweek = genericMethods.generateCurrentGameweek() + weekNumber

            while count <= nowGameweek:
                gameweekList.append(count)
                count += 1

            gameweekListClean = "/ "
            for week in gameweekList:
                gameweekListClean += f"{week} / "

            sortedTeamSumDifficultySet = sorted(listedDifficultyByTeam.items(), key=lambda x: sum(x[1]), reverse=False)
            sortedTeamSumDifficulty = list(map(lambda x:"-" if x==6 else x,sortedTeamSumDifficultySet))

            print("----------------------------------------------------------")
            print(f'Match difficulty for the next {weekNumber} games from easy to most difficult run:')
            print("")
            print(f"Gameweek: {gameweekListClean}")
            print("-------------------------------------------------------")
            print("")
            genericMethods.printDataClean(sortedTeamSumDifficulty, 20, '', '')
            print("----------------------------------------------------------")
            print("")


            endRoutine()

        if playerUserInputInitialInt == 8:
            print("----------------------------------------------------------------------------------------------")
            print("Do you want to see the highest value for money (most) or the poorest value for money (least)?:")
            print("")
            userInput = str.lower(input("> "))
            print("-----------------------------------------------------------------------------------------------")
            print("Running...")
            positions = playerData.generatePositionReference()
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            playerIDs = playerData.generatePlayersIdsList()
            playerNames = playerData.generatePlayerNameToIDMatching()
            pricePerPoint = playerData.generateListOfPointsPerPoundPerPlayerPerPosition()
            for positionName in positions:
                position = positions[positionName]
                positionData = pricePerPoint[position]
                playerPoundPerPoint = dict()
                for playerID in playerIDs:
                    player = playerNames[playerID].capitalize()
                    try:
                        if positionData[playerID] > 0:
                            playerPoundPerPoint[player] = round(positionData[playerID], 2)

                    except:
                        None
                        
                if userInput == 'most':
                    sortedAverageCost = sorted(playerPoundPerPoint.items(), key=lambda x: x[1], reverse=True) 
                    finalAverageCost = genericMethods.reformattedSortedTupleAsDict(sortedAverageCost)
                if userInput == 'least':
                    sortedAverageCost = sorted(playerPoundPerPoint.items(), key=lambda x: x[1], reverse=False)
                    finalAverageCost = genericMethods.reformattedSortedTupleAsDict(sortedAverageCost)
                else:
                    sortedAverageCost = sorted(playerPoundPerPoint.items(), key=lambda x: x[1], reverse=True)
                    finalAverageCost = genericMethods.reformattedSortedTupleAsDict(sortedAverageCost)


                print("----------------------------------------------------------")
                print(f'Top ranked {positionName}s for points per pound:')
                print("")
                genericMethods.printDataClean(finalAverageCost, 5, '', ' points per £M spent')
                print("----------------------------------------------------------")
                print("")

            endRoutine()

        if playerUserInputInitialInt == 9:                        
            print("----------------------------------------------------------------------------------------------")
            print("How many gameweeks do you want to see?")
            print("")
            userInput = int(input("> "))
            print("What is the max value you want to see?")
            print("")
            maxValue = float(input("> "))
            print("-----------------------------------------------------------------------------------------------")
            print("Initialising method...")
            nowGameweek = genericMethods.generateCurrentGameweek()
            fromGameweek = nowGameweek - userInput
            count = fromGameweek
            currentGameweek = nowGameweek - userInput
            playerIDs = playerData.generatePlayersIdsList()
            playerNames = playerData.generatePlayerNameToIDMatching()
            positions = playerData.generatePositionReferenceIDAsKey()
            sumOfPlayerScores = dict()
            allGameweekData = dict()
            gameweekList = list()

            while count <= nowGameweek:
                gameweekList.append(count)
                count += 1

            gameweekListClean = "/ "
            for week in gameweekList:
                gameweekListClean += f"{week} / "

            length = len(playerIDs) - 1
            for playerID in playerIDs:
                playerDataList = playerData.generateListOfPointsForNGameweeksPerPlayer(playerID, currentGameweek, nowGameweek, maxValue, 'int')
                sumOfPlayerScores[playerID] = sum(playerDataList)
                allGameweekData[playerID] = playerDataList

                currentIndex = list(playerIDs).index(playerID)
                genericMethods.runPercentage(length, currentIndex, 'Gathering player scores', 'Player score data gathered')                           
                            
            sortedByPosition = playerData.sortPlayerDataByPosition(allGameweekData)
            sortedSumByPosition = playerData.sortPlayerDataByPosition(sumOfPlayerScores)



            for position in sortedByPosition:
                positionName = positions[position]
                currentPositionData = sortedByPosition[position]
                sortedSumPoints = sorted(sortedSumByPosition[position].items(), key=lambda x: x[1], reverse=True)
                top5Players = sortedSumPoints[:5]
                finalSumPoints = genericMethods.reformattedSortedTupleAsDict(top5Players)
                top5PlayersPreviousGameweeks = dict()

                for player in finalSumPoints:
                    playerID = player
                    playerName = playerNames[playerID].capitalize()
                    top5PlayersPreviousGameweeks[playerName] = currentPositionData[playerID]

                numberOfGames = userInput + 1

                print("-----------------------------------------------------------------------------------------------------------")
                print(f'Top ranked {positionName}s for points over the last {numberOfGames} games (GW {fromGameweek} to {nowGameweek}):')
                print("")
                print(f"Gameweek: {gameweekListClean}")
                print("")
                for player in top5PlayersPreviousGameweeks:
                    playerDataTop5 = str(top5PlayersPreviousGameweeks[player]).replace("[","").replace("]","")
                    print(f"{player}: {playerDataTop5}")
                print("-----------------------------------------------------------------------------------------------------------")
                print("")
            endRoutine()

        if playerUserInputInitialInt == 10:
            gw = genericMethods.generateCurrentGameweek() + 1
            print("-----------------------------------------------------------------------------------------------------------")
            print(f'Which Gameweek do you want to see (next gameweek = {gw})?')
            print("-------------------------------------------------------")
            print("")
            gw = int(input("Gameweek >> "))
            nw = int(input("How many weeks to look in the future? >> "))
            easiestGames = Teams.gameweekDifficultyRankedForTeams(gw, nw)
            print("Indexed fixture difficulty by team where 100 is the easiest fixture:")
            for fixture in easiestGames:
                result = easiestGames[fixture]
                team = str.capitalize(fixture)
                index = int(round(genericMethods.indexValue(result,max(list(easiestGames.values())),min(list(easiestGames.values())),"n"), 0))
                print(f"{team}: {index}")


        if playerUserInputInitialInt == 11:
            goalEconomy = Teams.goalEconomyByTeam()

            teamNames = Teams.teamIDsAsKeysAndNamesAsData()

            finalGoalEconomy = dict()

            for team in goalEconomy:
                teamName = str.capitalize(teamNames[team])
                finalGoalEconomy[teamName] = round(goalEconomy[team], 1)

            orderedGoalEconomy = sorted(finalGoalEconomy.items(), key=lambda x: x[1], reverse=True)
            cleanGoalEconomy = genericMethods.reformattedSortedTupleAsDict(orderedGoalEconomy)

            print("-----------------------------------------------------")
            print("Goal Economy by team (% shots on target scored)")
            print("")
            genericMethods.printDataClean(cleanGoalEconomy, 20, "", "%")

            endRoutine()

        if playerUserInputInitialInt == 12:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(nextGameweek, True)

            print("")
            print(f"Estimate for goals conceded GW{nextGameweek}")
            print("")

            for teamName in nextGameLikelihoodtoConceed:
                goalsToBeconceded = nextGameLikelihoodtoConceed[teamName]
                print(f"{teamName}: {goalsToBeconceded}")

            endRoutine()

        if playerUserInputInitialInt == 13:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1
            nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(nextGameweek, True)

            print("")
            print(f"Estimate for goals scored GW{nextGameweek}")
            print("")

            for teamName in nextGameLikelihoodtoScore:
                goalsToBeScored = nextGameLikelihoodtoScore[teamName]
                print(f"{teamName}: {goalsToBeScored}")

            endRoutine()

        if playerUserInputInitialInt == 14:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1

            nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(nextGameweek, True)
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(nextGameweek, True)
            fixturesForGameweek = Teams.fixturesForGameweekByTeamID(nextGameweek)
            teamIdList = Teams.teamIDsAsKeysAndNamesAsData()

                                                
            print("----------------------------------------------------------------------------------------------")
            print("Would you like to see the actual results, or just who won?")
            print("[1] Winners only")
            print("[2] Full result")
            print("")
            userInput = int(input("> "))
            print("------------------------------")

            print(f"Estimated results based on past performance for GW{nextGameweek}:")

            for teamId in teamIdList:
                try:
                    away = fixturesForGameweek[teamId]
                    home = teamId
                                
                    homeName = teamIdList[home].capitalize()
                    homeScore = nextGameLikelihoodtoScore[homeName]
                    homeConceed = nextGameLikelihoodtoConceed[homeName]
                    homeNet = homeScore - homeConceed

                    awayName = teamIdList[away].capitalize()
                    awayScore = nextGameLikelihoodtoScore[awayName]
                    awayConceed = nextGameLikelihoodtoConceed[awayName]
                    awayNet = awayScore - awayConceed
                                
                    awayGoals = round(((awayScore + homeConceed) / 2), 1)
                    homeGoals = round(((homeScore + awayConceed) / 2), 1)
                    goalDifference = homeGoals - awayGoals

                    overallNet = homeNet - awayNet

                    if awayNet != 0 and homeNet != 0:
                        result = round((homeNet / awayNet), 1)
                    elif homeNet == 0:
                        result = round(awayNet, 1)
                    elif awayNet == 0:
                        result = round(homeNet, 1)
                                
                    if userInput == 1:
                        homeNameUpper = homeName.upper()
                        awayNameUpper = awayName.upper()
                        if overallNet > 0.65:
                            print(f"{homeNameUpper} VS {awayName}")

                        if -0.65 <= overallNet <= 0.65:
                            print(f"{homeName} DRAW {awayName}")
                                    
                        if overallNet < -0.65:
                            print(f"{homeName} VS {awayNameUpper}")

                    if userInput == 2:
                        if overallNet > 0.65:
                            print(f"{homeName} {homeGoals} vs {awayGoals} {awayName} = {result}")

                        if -0.65 <= overallNet <= 0.65:
                            print(f"{homeName} {homeGoals} vs {awayGoals} {awayName} = {result}")
                                    
                        if overallNet < -0.65:
                            print(f"{homeName} {homeGoals} vs {awayGoals} {awayName} = {result}")
                except:
                    None

        if playerUserInputInitialInt == 15:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1

            nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(nextGameweek, True)
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(nextGameweek, True)
            fixturesForGameweek = Teams.fixturesForGameweekByTeamID(nextGameweek)
            teamIdList = Teams.teamIDsAsKeysAndNamesAsData()

                                                
            print("----------------------------------------------------------------------------------------------")
            print("Would you like to see the actual results, or just who won?")
            print("[1] Winners only")
            print("[2] Full result")
            print("")
            userInput = int(input("> "))
            print("------------------------------")

            print(f"Estimated results based on past performance for GW{nextGameweek}:")

            for teamId in teamIdList:
                try:
                    away = fixturesForGameweek[teamId]
                    home = teamId
                                
                    homeName = teamIdList[home].capitalize()
                    homeScore = nextGameLikelihoodtoScore[homeName]
                    homeConceed = nextGameLikelihoodtoConceed[homeName]

                    awayName = teamIdList[away].capitalize()
                    awayScore = nextGameLikelihoodtoScore[awayName]
                    awayConceed = nextGameLikelihoodtoConceed[awayName]
                                    
                    awayGoals = (awayScore + homeConceed) / 2
                    homeGoals = (homeScore + awayConceed) / 2
                                    
                    awayGoalsRounded = int(round((awayScore + homeConceed) / 2, 0))
                    homeGoalsRounded = int(round((homeScore + awayConceed) / 2, 0))

                    goalDifference = int(round(homeGoals, 0) - round(awayGoals, 0))
                              
                    if userInput == 1:
                        homeNameUpper = homeName.upper()
                        awayNameUpper = awayName.upper()
                        if goalDifference >= 1:
                            print(f"{homeNameUpper} VS {awayName}")

                        if -1 < goalDifference < 1:
                            print(f"{homeName} DRAW {awayName}")
                                    
                        if goalDifference <= -1:
                            print(f"{homeName} VS {awayNameUpper}")

                    if userInput == 2:
                        if goalDifference >= 1:
                            print(f"{homeName} {homeGoalsRounded}-{awayGoalsRounded} {awayName}")

                        if -1 < goalDifference < 1:
                            print(f"{homeName} {homeGoalsRounded}-{awayGoalsRounded} {awayName}")
                                    
                        if goalDifference <= -1:
                            print(f"{homeName} {homeGoalsRounded}-{awayGoalsRounded} {awayName}")
                except:
                    None


            endRoutine()

        if playerUserInputInitialInt == 16:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1

            try:
                gameweekOfInterest = int(input(f"> What gameweek are you interested in? (next gameweek = {nextGameweek}) >> "))
            except:
                gameweekOfInterest = nextGameweek
                print(f"No gameweek specified: Running GW {nextGameweek}")

            decimalPlaces = int(input("> How many decimal places do you want the goals to? (0 = whole numbers) >> "))
            accountForInjuries = input("> Account for injuries? [Y/N] >> ")

            teamStrength = Teams.strengthHomeAndAwayByTeam()
            nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(gameweekOfInterest, True)
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(gameweekOfInterest, True)
            fixturesForGameweek = Teams.fixturesForGameweekByTeamID(gameweekOfInterest)
            teamIdList = Teams.teamIDsAsKeysAndNamesAsData()
            
            # POTENTIALLY REMOVE
            teamStrengthPercentage = Teams.teamIDsAsKeysAndPercentageStrengthAsData(gameweekOfInterest)
                                    
            print(f"Estimated results based on past performance for GW{gameweekOfInterest}:")
            

            for teamId in teamIdList:
                try:
                    away = fixturesForGameweek[teamId]
                    home = teamId

                    homeTeamStrength = teamStrength[home]
                    awayTeamStrength = teamStrength[away]
                                
                    homeTeamHomeStrength = homeTeamStrength['homeOverall']
                    homeTeamHomeStrengthAttack = homeTeamStrength['homeAttack']
                    homeTeamHomeStrengthDefence = homeTeamStrength['homeDefence']
                    homeStrengthPercentage = teamStrengthPercentage[home]

                    if accountForInjuries in ["Y", "y"]:
                        homeTeamAttackFactor = (homeTeamHomeStrengthAttack / homeTeamHomeStrength) * homeStrengthPercentage
                        homeTeamDefenceFactor = (homeTeamHomeStrengthDefence / homeTeamHomeStrength) * homeStrengthPercentage

                    else:
                        homeTeamAttackFactor = (homeTeamHomeStrengthAttack / homeTeamHomeStrength)
                        homeTeamDefenceFactor = (homeTeamHomeStrengthDefence / homeTeamHomeStrength)

                    awayTeamAwayStrength = awayTeamStrength['awayOverall']
                    awayTeamAwayStrengthAttack = awayTeamStrength['awayAttack']
                    awayTeamAwayStrengthDefence = awayTeamStrength['awayDefence']
                    awayStrengthPercentage = teamStrengthPercentage[away]

                    if accountForInjuries in ["Y", "y"]:
                        awayTeamAttackFactor = (awayTeamAwayStrengthAttack / awayTeamAwayStrength) * awayStrengthPercentage
                        awayTeamDefenceFactor = (awayTeamAwayStrengthDefence / awayTeamAwayStrength) * awayStrengthPercentage

                    else:
                        awayTeamAttackFactor = (awayTeamAwayStrengthAttack / awayTeamAwayStrength)
                        awayTeamDefenceFactor = (awayTeamAwayStrengthDefence / awayTeamAwayStrength)

                    homeName = teamIdList[home].capitalize()
                    homeScore = nextGameLikelihoodtoScore[homeName] * homeTeamAttackFactor
                    homeConceed = nextGameLikelihoodtoConceed[homeName] * homeTeamDefenceFactor

                    awayName = teamIdList[away].capitalize()
                    awayScore = nextGameLikelihoodtoScore[awayName] * awayTeamAttackFactor
                    awayConceed = nextGameLikelihoodtoConceed[awayName] * awayTeamDefenceFactor
                                    
                    awayGoals = (awayScore + homeConceed) / 2
                    homeGoals = (homeScore + awayConceed) / 2
    
                    awayGoalsRounded = float(round((awayScore + homeConceed) / 2, decimalPlaces))
                    homeGoalsRounded = float(round((homeScore + awayConceed) / 2, decimalPlaces))
                    
                    if decimalPlaces == 0:
                        awayGoalsRounded = int(awayGoalsRounded)
                        homeGoalsRounded = int(homeGoalsRounded)

                    awayRoundDiff = awayGoals - awayGoalsRounded
                    homeRoundDiff = homeGoals - homeGoalsRounded

                    homeConfidencePrint = ""
                    awayConfidencePrint = ""

                    if awayRoundDiff < 0:
                        awayRoundDiff = -awayRoundDiff

                    if homeRoundDiff < 0:
                        homeRoundDiff = -homeRoundDiff

                    if homeRoundDiff <= 0.25 and homeRoundDiff != 0:
                        homeConfidencePrint = "*"
                        
                    if awayRoundDiff <= 0.25 and awayRoundDiff != 0:
                        awayConfidencePrint = "*"

                    goalDifference = int(round(homeGoals, 0) - round(awayGoals, 0))
   
                    if goalDifference >= 1:
                        print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint}")

                    elif -1 < goalDifference < 1:
                        print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint}")
                                    
                    elif goalDifference <= -1:
                        print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint}")

                    else:
                        print(f"Not enough back data for: {homeName} vs {awayName}")
                        

                except:
                    None


            endRoutine()
                      
        if playerUserInputInitialInt == 17:
            maxGameweek = genericMethods.generateCurrentGameweek() + 1
            teamIdList = Teams.teamIDsAsKeysAndNamesAsData()
            currentGameweek = 1

            print("----------------------------------------------------------------------------------------------")
            print("Would you like to see the actual results, or just who won?")
            print("[1] Winners only")
            print("[2] Full result")
            print("")
            userInput = int(input("> "))
            print("------------------------------")

            while currentGameweek <= maxGameweek:
                print(f"Results for GW{currentGameweek}:")
                print("------------------------------")
                            
                results = Teams.resultsForGameweek(currentGameweek)
                fixtures = Teams.fixturesForGameweek(currentGameweek)

                for teamId in teamIdList:
                                
                    try:
                        homeName = teamIdList[teamId].capitalize()
                        awayId = fixtures[teamId]
                        awayName = teamIdList[awayId].capitalize()

                        homeResult = results[teamId]
                        awayResult = results[awayId]

                        if userInput == 1:
                            if homeResult > awayResult:
                                homeNameUpper = homeName.upper()
                                winner = f"{homeNameUpper}"

                            if homeResult == awayResult:
                                winner = "DRAW"

                            if homeResult < awayResult:
                                awayNameUpper = awayName.upper()
                                winner = f"{awayNameUpper}"

                            print(f"{winner}")

                        if userInput == 2:
                            print(f"({homeName}) {homeResult} vs {awayResult} ({awayName})")

                    except:
                        None

                currentGameweek += 1
                print("")
                print("------------------------------")


            endRoutine()

        if playerUserInputInitialInt == 18:
            currentGameweek = 1
            endGameweek = genericMethods.generateCurrentGameweek() + 1
            while currentGameweek <= endGameweek:
                nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(currentGameweek)
                nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(currentGameweek)
                fixturesForGameweek = Teams.fixturesForGameweekByTeamID(currentGameweek)
                teamIdList = Teams.teamIDsAsKeysAndNamesAsData()

                print(f"Estimated results based on past performance for GW{currentGameweek}:")

                for teamId in teamIdList:
                    try:
                        away = fixturesForGameweek[teamId]
                        home = teamId
                                
                        homeName = teamIdList[home].capitalize()
                        homeScore = nextGameLikelihoodtoScore[homeName]
                        homeConceed = nextGameLikelihoodtoConceed[homeName]
                        homeNet = homeScore - homeConceed
                        homeGoals = (homeScore + awayConceed) / 2

                        awayName = teamIdList[away].capitalize()
                        awayScore = nextGameLikelihoodtoScore[awayName]
                        awayConceed = nextGameLikelihoodtoConceed[awayName]
                        awayNet = awayScore - awayConceed
                        awayGoals = (awayScore + homeConceed) / 2
                        overallNet = homeNet - awayNet

                        goalDifference = homeGoals - awayGoals
                        if goalDifference < 0 :
                            goalDifference = - goalDifference

                        if awayNet != 0 and homeNet != 0:
                            result = round((homeNet / awayNet), 1)
                        elif homeNet == 0:
                            result = round(awayNet, 1)
                        elif awayNet == 0:
                            result = round(homeNet, 1)
                                
                        if overallNet > 0.65:
                            print(f"{homeName} {homeGoals} vs {awayGoals} {awayName} = {result}")

                        if -0.65 <= overallNet <= 0.65:
                            print(f"{homeName} {homeGoals} vs {awayGoals} {awayName} = {result}")
                                    
                        if overallNet < -0.65:
                            print(f"{homeName} {homeGoals} vs {awayGoals} {awayName} = {result}")
                    except:
                        None

                currentGameweek += 1

            endRoutine()

        if playerUserInputInitialInt == 19:
            currentGameweek = 2
            endGameweek = genericMethods.generateCurrentGameweek() + 1
            while currentGameweek <= endGameweek:
                nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(currentGameweek - 1)
                nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(currentGameweek - 1)
                fixturesForGameweek = Teams.fixturesForGameweekByTeamID(currentGameweek)
                teamIdList = Teams.teamIDsAsKeysAndNamesAsData()

                print(f"Estimated results based on past performance for GW{currentGameweek}:")

                for teamId in teamIdList:
                    try:
                        away = fixturesForGameweek[teamId]
                        home = teamId
                                
                        homeName = teamIdList[home].capitalize()
                        homeScore = nextGameLikelihoodtoScore[homeName]
                        homeConceed = nextGameLikelihoodtoConceed[homeName]

                        awayName = teamIdList[away].capitalize()
                        awayScore = nextGameLikelihoodtoScore[awayName]
                        awayConceed = nextGameLikelihoodtoConceed[awayName]
                                                                       
                        awayGoalsRounded = int(round((awayScore + homeConceed) / 2, 0 ))
                        homeGoalsRounded = int(round((homeScore + awayConceed) / 2, 0 ))

                        goalDifference = homeGoalsRounded - awayGoalsRounded
                        if goalDifference < 0 :
                            goalDifference = - goalDifference
                                
                        print(f"{homeName} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}")

                    except:
                        None

                currentGameweek += 1

            endRoutine()
                    
        if playerUserInputInitialInt == 20:
            currentGameweek = 2
            endGameweek = genericMethods.generateCurrentGameweek() + 1
            while currentGameweek <= endGameweek:
                nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(currentGameweek)
                nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(currentGameweek)
                fixturesForGameweek = Teams.fixturesForGameweekByTeamID(currentGameweek)
                teamIdList = Teams.teamIDsAsKeysAndNamesAsData()
                teamStrength = Teams.strengthHomeAndAwayByTeam()
                            
                print(f"Estimated results based on past performance for GW{currentGameweek}:")

                for teamId in teamIdList:
                    try:
                        away = fixturesForGameweek[teamId]
                        home = teamId

                        homeTeamStrength = teamStrength[home]
                        awayTeamStrength = teamStrength[away]
                                
                        homeTeamHomeStrength = homeTeamStrength['homeOverall']
                        homeTeamHomeStrengthAttack = homeTeamStrength['homeAttack']
                        homeTeamHomeStrengthDefence = homeTeamStrength['homeDefence']

                        homeTeamAttackFactor = homeTeamHomeStrengthAttack / homeTeamHomeStrength
                        homeTeamDefenceFactor = homeTeamHomeStrengthDefence / homeTeamHomeStrength
                                
                        awayTeamAwayStrength = awayTeamStrength['awayOverall']
                        awayTeamAwayStrengthAttack = awayTeamStrength['awayAttack']
                        awayTeamAwayStrengthDefence = awayTeamStrength['awayDefence']

                        awayTeamAttackFactor = awayTeamAwayStrengthAttack / awayTeamAwayStrength
                        awayTeamDefenceFactor = awayTeamAwayStrengthDefence / awayTeamAwayStrength

                        homeName = teamIdList[home].capitalize()
                        homeScore = nextGameLikelihoodtoScore[homeName] * homeTeamAttackFactor
                        homeConceed = nextGameLikelihoodtoConceed[homeName] * homeTeamDefenceFactor

                        awayName = teamIdList[away].capitalize()
                        awayScore = nextGameLikelihoodtoScore[awayName] * awayTeamAttackFactor
                        awayConceed = nextGameLikelihoodtoConceed[awayName] * awayTeamDefenceFactor
                                    
                        awayGoals = (awayScore + homeConceed) / 2
                        homeGoals = (homeScore + awayConceed) / 2
    
                        awayGoalsRounded = int(round((awayScore + homeConceed) / 2, 0))
                        homeGoalsRounded = int(round((homeScore + awayConceed) / 2, 0))
    
                        awayRoundDiff = awayGoals - awayGoalsRounded
                        homeRoundDiff = homeGoals - homeGoalsRounded

                        homeConfidencePrint = ""
                        awayConfidencePrint = ""

                        if awayRoundDiff < 0:
                            awayRoundDiff = -awayRoundDiff

                        if homeRoundDiff < 0:
                            homeRoundDiff = -homeRoundDiff

                        if homeRoundDiff <= 0.25 and homeRoundDiff != 0:
                            homeConfidencePrint = "*"
                        
                        if awayRoundDiff <= 0.25 and awayRoundDiff != 0:
                            awayConfidencePrint = "*"

                        goalDifference = int(round(homeGoals, 0) - round(awayGoals, 0))
   
                        if goalDifference >= 1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint}")

                        elif -1 < goalDifference < 1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint}")
                                    
                        elif goalDifference <= -1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint}")

                        else:
                            print(f"Not enough back data for: {homeName} vs {awayName}")
                        

                    except:
                        None

                currentGameweek += 1

            endRoutine()

        if playerUserInputInitialInt == 99:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1

            try:
                gameweekOfInterest = int(input(f"> What gameweek are you interested in? (next gameweek = {nextGameweek}) >> "))
            except:
                gameweekOfInterest = nextGameweek
                print(f"No gameweek specified: Running GW {nextGameweek}")

            teamStrength = Teams.strengthHomeAndAwayByTeam()
            nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(gameweekOfInterest, False)
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(gameweekOfInterest, False)
            fixturesForGameweek = Teams.fixturesForGameweekByTeamID(gameweekOfInterest)
            teamIdList = Teams.teamIDsAsKeysAndNamesAsData()
                        
            print(f"Estimated results based on past performance for GW{gameweekOfInterest}:")

            for teamId in teamIdList:
                try:
                    away = fixturesForGameweek[teamId]
                    home = teamId

                    homeTeamStrength = teamStrength[home]
                    awayTeamStrength = teamStrength[away]
                                
                    homeTeamHomeStrength = homeTeamStrength['homeOverall']
                    homeTeamHomeStrengthAttack = homeTeamStrength['homeAttack']
                    homeTeamHomeStrengthDefence = homeTeamStrength['homeDefence']

                    homeTeamAttackFactor = homeTeamHomeStrengthAttack / homeTeamHomeStrength
                    homeTeamDefenceFactor = homeTeamHomeStrengthDefence / homeTeamHomeStrength
                                
                    awayTeamAwayStrength = awayTeamStrength['awayOverall']
                    awayTeamAwayStrengthAttack = awayTeamStrength['awayAttack']
                    awayTeamAwayStrengthDefence = awayTeamStrength['awayDefence']

                    awayTeamAttackFactor = awayTeamAwayStrengthAttack / awayTeamAwayStrength
                    awayTeamDefenceFactor = awayTeamAwayStrengthDefence / awayTeamAwayStrength

                    homeName = teamIdList[home].capitalize()
                    homeScore = nextGameLikelihoodtoScore[homeName] * homeTeamAttackFactor
                    homeConceed = nextGameLikelihoodtoConceed[homeName] * homeTeamDefenceFactor

                    awayName = teamIdList[away].capitalize()
                    awayScore = nextGameLikelihoodtoScore[awayName] * awayTeamAttackFactor
                    awayConceed = nextGameLikelihoodtoConceed[awayName] * awayTeamDefenceFactor
                                    
                    awayGoals = (awayScore + homeConceed) / 2
                    homeGoals = (homeScore + awayConceed) / 2
    
                    awayGoalsRounded = int(round((awayScore + homeConceed) / 2, 0))
                    homeGoalsRounded = int(round((homeScore + awayConceed) / 2, 0))
    
                    awayRoundDiff = awayGoals - awayGoalsRounded
                    homeRoundDiff = homeGoals - homeGoalsRounded

                    homeConfidencePrint = ""
                    awayConfidencePrint = ""

                    if awayRoundDiff < 0:
                        awayRoundDiff = -awayRoundDiff

                    if homeRoundDiff < 0:
                        homeRoundDiff = -homeRoundDiff

                    if homeRoundDiff <= 0.25 and homeRoundDiff != 0:
                        homeConfidencePrint = "*"
                        
                    if awayRoundDiff <= 0.25 and awayRoundDiff != 0:
                        awayConfidencePrint = "*"

                    netVariance = round(awayRoundDiff + homeRoundDiff, 2)

                    goalDifference = int(round(homeGoals, 0) - round(awayGoals, 0))
   
                    if goalDifference >= 1:
                        print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint} >> {netVariance}")

                    elif -1 < goalDifference < 1:
                        print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint} >> {netVariance}")
                                    
                    elif goalDifference <= -1:
                        print(f"{homeName}{homeConfidencePrint} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}{awayConfidencePrint} >> {netVariance}")

                    else:
                        print(f"Not enough back data for: {homeName} vs {awayName}")
                        

                except:
                    None


            endRoutine()
                      

        if playerUserInputInitialInt == 100:
                        
            nextGameweek = genericMethods.generateCurrentGameweek() + 1

            try:
                gameweekOfInterest = int(input(f"> What gameweek are you interested in? (next gameweek = {nextGameweek}) >> "))
            except:
                gameweekOfInterest = nextGameweek
                print(f"No gameweek specified: Running GW {nextGameweek}")

            teamStrength = Teams.strengthHomeAndAwayByTeam()
            nextGameLikelihoodtoScoreOutlier = Teams.generateLikelihoodToScoreByTeamForNextGame(gameweekOfInterest, True)
            nextGameLikelihoodtoConceedOutlier = Teams.generateLikelihoodToConceedByTeamForNextGame(gameweekOfInterest, True)
            nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(gameweekOfInterest, False)
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(gameweekOfInterest, False)
            fixturesForGameweek = Teams.fixturesForGameweekByTeamID(gameweekOfInterest)
            teamIdList = Teams.teamIDsAsKeysAndNamesAsData()
            teamStrengthPercentage = Teams.teamIDsAsKeysAndPercentageStrengthAsData(gameweekOfInterest)

            decimalPlaces = int(input("> How many decimal places do you want the goals to? (0 = whole numbers) >> "))
            printType = int(input("Do you want all of the details [1] or ready for twitter [2]? >> (Type 1 or 2) >>"))

            print(f"Estimated results based on past performance for GW{gameweekOfInterest}:")
            for teamId in teamIdList:
                try:
                    away = fixturesForGameweek[teamId]
                    home = teamId

                    homeTeamStrength = teamStrength[home]
                    awayTeamStrength = teamStrength[away]
                                
                    homeTeamHomeStrength = homeTeamStrength['homeOverall']
                    homeTeamHomeStrengthAttack = homeTeamStrength['homeAttack']
                    homeTeamHomeStrengthDefence = homeTeamStrength['homeDefence']
                    homeStrengthPercentage = teamStrengthPercentage[home]

                    homeTeamAttackFactor = (homeTeamHomeStrengthAttack / homeTeamHomeStrength)
                    homeTeamDefenceFactor = (homeTeamHomeStrengthDefence / homeTeamHomeStrength)
                                
                    awayTeamAwayStrength = awayTeamStrength['awayOverall']
                    awayTeamAwayStrengthAttack = awayTeamStrength['awayAttack']
                    awayTeamAwayStrengthDefence = awayTeamStrength['awayDefence']
                    awayStrengthPercentage = teamStrengthPercentage[away]

                    awayTeamAttackFactor = (awayTeamAwayStrengthAttack / awayTeamAwayStrength)
                    awayTeamDefenceFactor = (awayTeamAwayStrengthDefence / awayTeamAwayStrength)

                    homeName = teamIdList[home].capitalize()
                    homeScore = nextGameLikelihoodtoScore[homeName] * homeTeamAttackFactor
                    homeConceed = nextGameLikelihoodtoConceed[homeName] * homeTeamDefenceFactor
                    homeScoreOutlier = nextGameLikelihoodtoScoreOutlier[homeName] * homeTeamAttackFactor
                    homeConceedOutlier = nextGameLikelihoodtoConceedOutlier[homeName] * homeTeamDefenceFactor

                    awayName = teamIdList[away].capitalize()
                    awayScore = nextGameLikelihoodtoScore[awayName] * awayTeamAttackFactor
                    awayConceed = nextGameLikelihoodtoConceed[awayName] * awayTeamDefenceFactor
                    awayScoreOutlier = nextGameLikelihoodtoScoreOutlier[awayName] * awayTeamAttackFactor
                    awayConceedOutlier = nextGameLikelihoodtoConceedOutlier[awayName] * awayTeamDefenceFactor

                    # Without outliers:

                    awayGoals = (awayScore + homeConceed) / 2
                    homeGoals = (homeScore + awayConceed) / 2

                    awayGoalsRounded = float(round((awayScore + homeConceed) / 2, decimalPlaces))
                    homeGoalsRounded = float(round((homeScore + awayConceed) / 2, decimalPlaces))
    
                    if decimalPlaces == 0:
                        awayGoalsRounded = int(awayGoalsRounded)
                        homeGoalsRounded = int(homeGoalsRounded)

                    awayRoundDiff = awayGoals - round(awayGoals, 0)
                    homeRoundDiff = homeGoals - round(homeGoals, 0)

                    homeConfidencePrint = ""
                    awayConfidencePrint = ""

                    if awayRoundDiff < 0:
                        awayRoundDiff = -awayRoundDiff

                    if homeRoundDiff < 0:
                        homeRoundDiff = -homeRoundDiff

                    if homeRoundDiff <= 0.25 and homeRoundDiff != 0:
                        homeConfidencePrint = "*"
                        
                    if awayRoundDiff <= 0.25 and awayRoundDiff != 0:
                        awayConfidencePrint = "*"

                    netVariance = round(awayRoundDiff + homeRoundDiff, 2)

                    # With outliers:
    
                    awayGoalsOutlier = (awayScoreOutlier + homeConceedOutlier) / 2
                    homeGoalsOutlier = (homeScoreOutlier + awayConceedOutlier) / 2
                    
                    
                    awayGoalsRoundedOutlier = float(round((awayScoreOutlier + homeConceedOutlier) / 2, decimalPlaces))
                    homeGoalsRoundedOutlier = float(round((homeScoreOutlier + awayConceedOutlier) / 2, decimalPlaces))

                    if decimalPlaces == 0:
                        awayGoalsRoundedOutlier = int(awayGoalsRoundedOutlier)
                        homeGoalsRoundedOutlier = int(homeGoalsRoundedOutlier)

                    awayRoundDiffOutlier = awayGoalsOutlier - round(awayGoalsOutlier, 0)
                    homeRoundDiffOutlier = homeGoalsOutlier - round(homeGoalsOutlier, 0)

                    homeConfidencePrintOutlier = ""
                    awayConfidencePrintOutlier = ""

                    if awayRoundDiffOutlier < 0:
                        awayRoundDiffOutlier = -awayRoundDiffOutlier

                    if homeRoundDiffOutlier < 0:
                        homeRoundDiffOutlier = -homeRoundDiffOutlier

                    if homeRoundDiffOutlier <= 0.25 and homeRoundDiffOutlier != 0:
                        homeConfidencePrintOutlier = "^"
                        
                    if awayRoundDiffOutlier <= 0.25 and awayRoundDiffOutlier != 0:
                        awayConfidencePrintOutlier = "^"

                    netVarianceOutlier = round(awayRoundDiffOutlier + homeRoundDiffOutlier, 2)

                    # If variance larger

                    if netVariance > netVarianceOutlier:
                        homeGoalsPrint = homeGoalsRounded
                        awayGoalsPrint = awayGoalsRounded
                        homeConfidencePrint = homeConfidencePrint
                        awayConfidencePrint = awayConfidencePrint
                        netVariancePrint = netVariance
                        netVarianceDelta = round(netVariance - netVarianceOutlier,2)
                        indicator = "[X]"

                    elif netVariance < netVarianceOutlier:
                        homeGoalsPrint = homeGoalsRoundedOutlier
                        awayGoalsPrint = awayGoalsRoundedOutlier
                        homeConfidencePrint = homeConfidencePrintOutlier
                        awayConfidencePrint = awayConfidencePrintOutlier
                        netVariancePrint = netVarianceOutlier
                        netVarianceDelta = round(netVarianceOutlier - netVariance,2)
                        indicator = "[Z]"

                    else:
                        homeGoalsPrint = homeGoalsRounded
                        awayGoalsPrint = awayGoalsRounded
                        homeConfidencePrint = homeConfidencePrint
                        awayConfidencePrint = awayConfidencePrint
                        netVariancePrint = netVariance
                        netVarianceDelta = round(netVariance - netVarianceOutlier,2)
                        indicator = "[-]"

                    goalDifference = int(round(homeGoals, 0) - round(awayGoals, 0))
                    
                    if printType == 1:
                        if goalDifference >= 1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsPrint} vs {awayGoalsPrint} {awayName}{awayConfidencePrint} >> {netVariance} // Difference: {netVarianceDelta} - {indicator}")

                        elif -1 < goalDifference < 1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsPrint} vs {awayGoalsPrint} {awayName}{awayConfidencePrint} >> {netVariance} // Difference: {netVarianceDelta} - {indicator}")
                                    
                        elif goalDifference <= -1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsPrint} vs {awayGoalsPrint} {awayName}{awayConfidencePrint} >> {netVariance} // Difference: {netVarianceDelta} - {indicator}")

                        else:
                            print(f"Not enough back data for: {homeName} vs {awayName}")

                    else:
                        if goalDifference >= 1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsPrint} vs {awayGoalsPrint} {awayName}{awayConfidencePrint}")

                        elif -1 < goalDifference < 1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsPrint} vs {awayGoalsPrint} {awayName}{awayConfidencePrint}")
                                    
                        elif goalDifference <= -1:
                            print(f"{homeName}{homeConfidencePrint} {homeGoalsPrint} vs {awayGoalsPrint} {awayName}{awayConfidencePrint}")

                        else:
                            print(f"Not enough back data for: {homeName} vs {awayName}")

                except:
                    None


            endRoutine()


def experimentalRoutine():
    print("-----------------------------------------------------------------------")
    print("What method did you want to test?")
    print("!! PLEASE SELECT A NUMBER")
    print("-----------------------------------------------------------------------")
    print(" [1] Gather goal economy by team by week")
    print("-----------------------------------------------------------------------")
    print("")
    print("What do you want to see?")
    playerUserInputInitial = int(input(">"))
    if playerUserInputInitial == 1:
        currentWeek = 1
        lastWeek = genericMethods.generateCurrentGameweek()
        goalEconomyByGameweek = dict()
        while currentWeek <= lastWeek:
            # Team ref list: TODO: Delete when adding as full method
            teamIDs = Teams.teamIDsAsKeysAndNamesAsData()
            goalEconomyThisWeek = Teams.goalEconomyByTeamForGameweek(currentWeek)
            goalEconomyByGameweek[currentWeek] = goalEconomyThisWeek
            genericMethods.runPercentage(lastWeek,currentWeek,f"Running week {currentWeek} of {lastWeek}", "All of the weeks have now been run successfully")
            currentWeek += 1

        endRoutine()


        

# Gameweek specific section of the program. Contains the menu items for the gameweek part of the console app
def gameweekRoutine():
    print("------------------------------------------------------------------------")
    print("You've said you want to take a look at the gameweek data. You can look at:")
    print("!! PLEASE SELECT A NUMBER")
    print("------------------------------------------------------------------------")
    print(" [1] All players printed in console")
    print(" [2] A player (by surname)")
    print(" [3] A comma seperated list of playes (by surname)")
    print(" [4] Top 10 net transfers in this week")
    print(" [5] Top 10 net transfers out this week")
    print("------------------------------------------------------------------------")
    print(" [99] Print all player data to console")
    print(" [101] Export all player data to excel")
    print("------------------------------------------------------------------------")
    print("")
    print("What would you like to see?:")
    playerUserInputInitial = input(">")
    print("")
    genericMethods.parse(playerUserInputInitial)

    if genericMethods.isInt(playerUserInputInitial) == True:
        playerUserInputInitialInt = int(playerUserInputInitial)
        if playerUserInputInitialInt == 1:
            gameweekSummaryListFull = playerData.generatePlayersFullNameList()
            print("------------------------------------")
            print("How would you like to see the output?")
            print("------------------------------------")
            print(" [1] Full list")
            print(" [2] Comma seperated list  of surnames")
            print("------------------------------------")
            playerListInput = input(" > ")
            # try and put the input in as an integer
            genericMethods.parse(playerListInput)
            if genericMethods.isInt(playerListInput):
                if int(playerListInput) == 1:
                    for player in gameweekSummaryListFull:
                        print(player)
                elif int(playerListInput) == 2:
                    gameweekSummaryListCleaned = str(gameweekSummaryListFull).replace("'","").replace("[","").replace("]","")
                    print(gameweekSummaryListCleaned)
                    copyTo = Tk()
                    copyTo.clipboard_clear()
                    copyTo.clipboard_append(gameweekSummaryListCleaned)
                    copyTo.update()
                    copyTo.destroy()
                    print("")
                    print("// This has been copied to your clipboard.")
                    print("")
                else:
                    print("======================================================================================")
                    print("!! ERROR:Command wasn't recognised- please pick one of the above options and try again:")
                    print("======================================================================================")
                    print("")

            else:
                print("====================================================================================")
                print("!! ERROR:Input was not a number - please pick one of the above options and try again:")
                print("====================================================================================")
                print("")
            endRoutine()

        elif playerUserInputInitialInt == 2:
            print("----------------------------------")
            print("Let us know who you're looking for:")
            print("!! TYPE IN A SURNAME")
            print("----------------------------------")
            playerSurname = str.lower(input("> "))
            gameweekSummary.playerInfoBySurname(playerSurname)
            endRoutine()
                    
        elif playerUserInputInitialInt == 3:
            print("-----------------------------------------------------------------------------------------------------")
            print("Let us know who you're looking for in the format \"surname,surname,surname\" e.g. salah,sterling,kane:")
            print("!! TYPE IN THE SURNAMES")
            print("-----------------------------------------------------------------------------------------------------")
            playerSurnameList = str.lower(input("> "))
            playerListNew = list()
            playerList = list()
            playerListNew = playerSurnameList.split(",")
            for i in playerListNew:
                playerList.append(i.strip())
            for playerSurname in playerList:
                gameweekSummary.playerInfoBySurname(playerSurname)
            endRoutine()
                        

        elif playerUserInputInitialInt == 4:
            print("-------------------------------------------")
            print("How many players do you want to see (e.g. for \"Top 10\" type 10):")
            print("!! TYPE IN A NUMBER")
            print("-------------------------------------------")
            numberOfRecordsToShow = int(input("> "))
            topTransfers = gameweekSummary.mostNetTransfersIn(numberOfRecordsToShow)
            topTransfersFormatted = genericMethods.reformattedSortedTupleAsDict(topTransfers)
            currentGameweek = genericMethods.generateCurrentGameweek() + 1
            print("--------------------------------------------")
            print(f'Top {numberOfRecordsToShow} transfers in for GW{currentGameweek}:')
            print("")
            genericMethods.printDataClean(topTransfersFormatted, numberOfRecordsToShow, "", "")
            print("--------------------------------------------")
            print("")
            endRoutine()

        elif playerUserInputInitialInt == 5:
            print("-------------------------------------------")
            print("How many players do you want to see (e.g. for \"Top 10\" type 10:))")
            print("!! TYPE IN A NUMBER")
            print("-------------------------------------------")
            numberOfRecordsToShow = int(input("> "))
            topTransfers =  gameweekSummary.mostNetTransfersOut(numberOfRecordsToShow)
            topTransfersFormatted = genericMethods.reformattedSortedTupleAsDict(topTransfers)
            currentGameweek = genericMethods.generateCurrentGameweek() + 1
            print("--------------------------------------------")
            print(f'Top {numberOfRecordsToShow} transfers out for GW{currentGameweek}:')
            print("")
            genericMethods.printDataClean(topTransfersFormatted, numberOfRecordsToShow, "", "")
            print("--------------------------------------------")
            print("")
            endRoutine()

        elif playerUserInputInitialInt == 99:
            gameweekSummary.printAllData(gameweekSummarySub, playersFileName)

        elif playerUserInputInitialInt == 101:
            gameweekSummary.exportToExcelPlayers()
            endRoutine()

        else:
            print("====================================================================================")
            print("!! ERROR:Command not recognised - please pick one of the above options and try again:")
            print("====================================================================================")
            print("")
            playerRoutine()

    else:
        print("====================================================================================")
        print("!! ERROR:Input was not a number - please pick one of the above options and try again:")
        print("====================================================================================")
        print("")
        playerRoutine()

# Start the program

print("")
print("==============================")
print(" ________  _______   _____")
print("|_   __  ||_   __ \ |_   _|")
print("  | |_ \_|  | |__) |  | |")  
print("  |  _|     |  ___/   | |   _")  
print(" _| |_     _| |_    _ | |__/ |") 
print("|_____|   |_____|   |________|")
print("")
print("V.2.5.1")
print("")
print("==============================")
print("")
print("Welcome to the FPL console app for data extraction.")
print("")

introRoutine()
