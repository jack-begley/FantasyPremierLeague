import gameweekSummary
import playerData
import genericMethods
import Teams
import operator
import requests
import tkinter as Tk
import sys, traceback
from collections import OrderedDict


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
myTeamString = "2923192/1/live"
myTeam = 2923192
userInput = ""
playersFileName = "players"

# League Codes:

tygwyn = 'wo7rlj'
brooks = 'sgvzsa'
savanta = 'op3f9m'
mrsbaines = 'yanfqi'

tygwynID = 856255
brooksID = 699088
savantaID = 806190
mrsbainesID = 1164443

# Quit the program if the user decides they want to leave
def endRoutine():
    print("// Would you like to run another function?")
    print("Y/N:")

    finalDecision = str.lower(input("> "))

    if finalDecision == "y":
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
            
        if userInputInt ==  2:
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

        #TODO: Test all active URLs, Repair "Teams" URL
        # printAllData(teams, "team")

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
    print(" [2] All gameweek data for a player (by surname)")
    print(" [3] All player data by gameweek (number)")
    print(" [4] Create predictions of performance for next gameweek")
    print(" [5] IN PROGRESS: Generate list of player metrics that relate to performance")
    print("")
    print(" Data Exports: ")
    print(" [6] All player data for all gameweeks (to excel)")
    print("")
    print(" TEST:")
    print(" [99] Test: Rank player performance")
    print(" [100] Test: How previous performance affects future performance")
    print("------------------------------------------------------------------------")
    print("")
    print("What would you like to see?:")
    playerUserInputInitial = input(">")
    print("")
    genericMethods.parse(playerUserInputInitial)

    if genericMethods.isInt(playerUserInputInitial) == True:
        playerUserInputInitialInt = int(playerUserInputInitial)
        if playerUserInputInitialInt == 1:
            print("-----------------------------------")
            print("Let us know who you're looking for:")
            print("!! TYPE IN A SURNAME")
            print("-----------------------------------")
            playerSurname = str.lower(input("> "))
            gameweekSummary.playerInfoBySurname(playerSurname)
            endRoutine()

        if playerUserInputInitialInt == 2:
            print("-----------------------------------")
            print("Let us know who you're looking for:")
            print("!! TYPE IN A SURNAME")
            print("-----------------------------------")
            playerSurname = str.lower(input("> "))
            playerDataFile = playerData.allPlayerDataBySurname(playerSurname)
            print("")
            print("-----------------------------------")
            print("Would you like to export the data?:")
            print("!! TYPE IN Y/N")
            print("-----------------------------------")
            userInput = str.lower(input("> "))
            if userInput == 'y':
                gameweekHeaders = generateCommaSeperatedGameweekNumberList()
                genericMethods.printListToExcel(playerDataFile, gameweekHeaders)
            else:
                endRoutine()

        elif playerUserInputInitialInt == 3:
            print("-------------------------------------------")
            print("Let us know what week you're interested in:")
            print("!! TYPE IN A GAMEWEEK NUMBER")
            print("-------------------------------------------")
            gameweekNumber = str.lower(input("> "))
            playerOutput = playerData.gatherGameweekDataByPlayer(gameweekNumber)
            for player in playerOutput:
                print(f'{player}: {playerOutput[player]}')
            endRoutine()

        elif playerUserInputInitialInt == 4:
            gameweekNumber = genericMethods.generateCurrentGameweek()
            currentGameweek = gameweekNumber - 6
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

        elif playerUserInputInitialInt == 5:
            print("--------------------------------------------------------")
            print("Let us know how many weeks you want to look back across:")
            print("!! TYPE IN A NUMBER")
            print("--------------------------------------------------------")
            userInputGameweekDifference = int(input("> "))
            print("Running...")
            positions = playerData.generatePositionReference()
            maxGameweek = genericMethods.generateCurrentGameweek()
            currentGameweek = maxGameweek - userInputGameweekDifference
            teamIDs = Teams.teamIDsAsKeysAndNamesAsData()
            playerIDs = playerData.generatePlayersIdsList()
            playerNames = playerData.generatePlayerNameToIDMatching()
            scoreByGameweek = dict()
            while currentGameweek <= maxGameweek:
                scoreByTeams = dict()
                for teamID in teamIDs:
                    scoreByPlayers = dict()
                    currentPlayersList = Teams.generateListOfPlayerIDsAsKeysForTeam(teamID)
                    team = teamIDs[teamID].capitalize()
                    for playerID in currentPlayersList:
                        player = playerNames[playerID].capitalize()
                        scoreByPlayers[player] = playerData.generateListOfPlayersAndMetricsRelatedToPerformance(playerID, currentGameweek)

                    scoreByTeams[team] = scoreByPlayers
                            
                scoreByGameweek[currentGameweek] = scoreByTeams

                currentGameweek += 1


            endRoutine()


        elif playerUserInputInitialInt == 6:
            playerIDs = gameweekSummary.generatePlayerIDs()
            playerData.exportPlayerDataByGameweek(playerIDs)
                        
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
    print(" [1] My team")
    print(" [2] All weeks performance for a given team")
    print(" [3] Single team summary")
    print(" [4] Performance stats for a gameweek for a given team (TODO: add stats for players that week too)")
    print(" [5] Login and see top teams picks league")
    print(" [6] Average cost of position by team")
    print(" [7] Average game difficulty for the next N games ranked for all teams")
    print(" [8] Top 5 players by position for points per pound")
    print(" [9] Top performers by position for last N gameweeks")
    print("")
    print(" Goal and Result predictions")
    print("")
    print(" [10] Average goals conceeded by team for difficulty this week")
    print(" [11] Average goals scored by team for difficulty this week")
    print(" [12] Predicting next gameweek results")
    print(" [13] Predicting next gameweek results based on goals")
    print(" [14] Weighted predictions for next gameweek based on goals")
    print("")
    print(" Historical Results: ")
    print("")
    print(" [15] Results by gameweek")
    print(" [16] Predictions for historical gameweeks")
    print(" [17] Predictions for historical gameweeks based on goals")
    print(" [18] Weighted predictions for historical gameweeks based on goals")
    print("")
    print(" TEST:")
    print(" [19] Top performers by position for last N gameweeks with gameweek difficulty (and next gameweek difficulty?)")
    print(" [20] Players by Influence")
    print("")
    print("------------------------------------------------------------------------")
    print("")
    print("What would you like to see?:")
    playerUserInputInitial = input(">")
    print("")
    genericMethods.parse(playerUserInputInitial)

    if genericMethods.isInt(playerUserInputInitial) == True:
        playerUserInputInitialInt = int(playerUserInputInitial)

        if playerUserInputInitialInt == 1:
            print("-----------------------------------")
            print("Please log into your account to access league data:")
            print("")
            username = input("Email: ")
            password = input("Password: ")
            currentTeam = Teams.getTeamDetails(2923192, username, password)
            endRoutine()                    
                    
        if playerUserInputInitialInt == 2:
            print("-----------------------------------")
            print("Please type the team name in that you want to see data for:")
            print("")
            userInput = str.lower(input("> "))
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            teamID = teamNames[userInput]
            teamIDsAndNames = Teams.teamIDsAsKeysAndNamesAsData()
            currentTeamName = Teams.teamIDsAndNames[teamID]
            performanceSummary = Teams.performanceSummaryForTeam(teamID)

            endRoutine()

        if playerUserInputInitialInt == 3:
            print("-----------------------------------")
            print("Please type the team name in that you want to see data for:")
            print("")
            userInput = str.lower(input("> "))
            teamNames = Teams.teamNamesAsKeysAndIDsAsData()
            teamID = teamNames[userInput]
            Teams.printTeamDataToConsole(teamID)
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
                currentTeamData = Teams.getTeamDetails(id, username, password)
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
            print(f'Top 20 players picked by best performers for GW{currentGameweek}:')
            print("")
            genericMethods.printDataClean(finalPlayers, 20, '', '%')
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
                listedGameweekDifficulty = Teams.upcomingGameDifficultyListed(weekNumber, currentTeamID)
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

            sortedTeamSumDifficulty = sorted(listedDifficultyByTeam.items(), key=lambda x: sum(x[1]), reverse=False)
            sortedTeamAverageDifficultyList = OrderedDict()

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
                playerDataList = playerData.generateListOfPointsForNGameweeksPerPlayer(playerID, currentGameweek, nowGameweek)
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
                print("-------------------------------------------------------")
                for player in top5PlayersPreviousGameweeks:
                    playerDataTop5 = str(top5PlayersPreviousGameweeks[player]).replace("[","").replace("]","")
                    print(f"{player}: {playerDataTop5}")
                print("-----------------------------------------------------------------------------------------------------------")
                print("")
            endRoutine()

        if playerUserInputInitialInt == 10:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(nextGameweek)

            print("")
            print(f"Estimate for goals conceeded GW{nextGameweek}")
            print("")

            for teamName in nextGameLikelihoodtoConceed:
                goalsToBeConceeded = nextGameLikelihoodtoConceed[teamName]
                print(f"{teamName}: {goalsToBeConceeded}")

            endRoutine()

        if playerUserInputInitialInt == 11:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1
            nextGameLikelihoodtoScore = Teams.generateLikelihoodToScoreByTeamForNextGame(nextGameweek)

            print("")
            print(f"Estimate for goals scored GW{nextGameweek}")
            print("")

            for teamName in nextGameLikelihoodtoScore:
                goalsToBeScored = nextGameLikelihoodtoScore[teamName]
                print(f"{teamName}: {goalsToBeScored}")

            endRoutine()

        if playerUserInputInitialInt == 12:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1

            nextGameLikelihoodtoScore =Teams. generateLikelihoodToScoreByTeamForNextGame(nextGameweek)
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(nextGameweek)
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

        if playerUserInputInitialInt == 13:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1

            nextGameLikelihoodtoScore =Teams. generateLikelihoodToScoreByTeamForNextGame(nextGameweek)
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(nextGameweek)
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

        if playerUserInputInitialInt == 14:
            nextGameweek = genericMethods.generateCurrentGameweek() + 1

            teamStrength = Teams.strengthHomeAndAwayByTeam()
            nextGameLikelihoodtoScore =Teams. generateLikelihoodToScoreByTeamForNextGame(nextGameweek)
            nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(nextGameweek)
            fixturesForGameweek = Teams.fixturesForGameweekByTeamID(nextGameweek)
            teamIdList = Teams.teamIDsAsKeysAndNamesAsData()
                        
            print(f"Estimated results based on past performance for GW{nextGameweek}:")

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

                    awayTeamAttackFactor = awayTeamHomeStrengthAttack / awayTeamAwayStrength
                    awayTeamDefenceFactor = awayTeamHomeStrengthDefence / awayTeamAwayStrength

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

                    goalDifference = int(round(homeGoals, 0) - round(awayGoals, 0))
   
                    if goalDifference >= 1:
                        print(f"{homeName} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}")

                    if -1 < goalDifference < 1:
                        print(f"{homeName} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}")
                                    
                    if goalDifference <= -1:
                        print(f"{homeName} {homeGoalsRounded} vs {awayGoalsRounded} {awayName}")

                except:
                    None


            endRoutine()
                      
        if playerUserInputInitialInt == 15:
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

        if playerUserInputInitialInt == 16:
            currentGameweek = 1
            endGameweek = genericMethods.generateCurrentGameweek() + 1
            while currentGameweek <= endGameweek:
                nextGameLikelihoodtoScore =Teams. generateLikelihoodToScoreByTeamForNextGame(currentGameweek)
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

        if playerUserInputInitialInt == 17:
            currentGameweek = 2
            endGameweek = genericMethods.generateCurrentGameweek() + 1
            while currentGameweek <= endGameweek:
                nextGameLikelihoodtoScore =Teams. generateLikelihoodToScoreByTeamForNextGame(currentGameweek - 1)
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
                    
        if playerUserInputInitialInt == 18:
            currentGameweek = 2
            endGameweek = genericMethods.generateCurrentGameweek() + 1
            while currentGameweek <= endGameweek:
                nextGameLikelihoodtoScore =Teams. generateLikelihoodToScoreByTeamForNextGame(currentGameweek - 1)
                nextGameLikelihoodtoConceed = Teams.generateLikelihoodToConceedByTeamForNextGame(currentGameweek - 1)
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

        if playerUserInputInitialInt == 19:                        
            print("----------------------------------------------------------------------------------------------")
            print("How many gameweeks do you want to see?")
            print("")
            userInput = int(input("> "))
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
                playerDataList = playerData.generateListOfPointsForNGameweeksPerPlayer(playerID, currentGameweek, nowGameweek)
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
                print("-------------------------------------------------------")
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
                    
        if playerUserInputInitialInt == 20:
            currentGameweek = genericMethods.generateCurrentGameweek()
            print("Gathering player influence scores...")
            playersByInfluence = playerData.playerInfluence(currentGameweek)
            playerNames = playerData.generatePlayerNameToIDMatching()

            print("-----------------------------------------------------------------------------------------------------------")
            print(f'Top ranked players for points for GW{currentGameweek}:')
            print("")
            print("-------------------------------------------------------")
            for player in playersByInfluence:
                playerName = str(playerNames[player]).capitalize()
                playerInfluence = playersByInfluence[player]
                print(f"{playerName}: {playerInfluence}")

            endRoutine()

def experimentalRoutine():
    print("-----------------------------------------------------------------------")
    print("What method did you want to test?")
    print("!! PLEASE SELECT A NUMBER")
    print("-----------------------------------------------------------------------")
    print(" [1] Gather goal economy by team by week")
    print(" [2] Goal economy by gameweek difficulty")
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

    if playerUserInputInitial == 2:
        goalEconomy = Teams.goalEconomyByTeam()

        teamNames = Teams.teamIDsAsKeysAndNamesAsData()

        finalGoalEconomy = dict()

        for team in goalEconomy:
            teamName = str.capitalize(teamNames[team])
            finalGoalEconomy[teamName] = round(goalEconomy[team], 1)

        orderedGoalEconomy = sorted(finalGoalEconomy.items(), key=lambda x: x[1], reverse=True)
        cleanGoalEconomy = genericMethods.reformattedSortedTupleAsDict(orderedGoalEconomy)

        print("-----------------------------------------------------")
        print("Goal Economy by team (goals scored / shots on target)")
        print("")
        genericMethods.printDataClean(cleanGoalEconomy, 20, "", "%")


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
print("V.0.5.101")
print("")
print("==============================")
print("")
print("Welcome to the FPL console app for data extraction.")
print("")

introRoutine()
