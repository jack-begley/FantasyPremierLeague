import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import requests
import json
import genericMethods
import playerData
import gameweekSummary
import Teams
from requests.auth import HTTPBasicAuth



# Verifies Auth to allow users to activate URLs that require login
def loginToSecureURL(urlResponseToReturn, username, password):
    session = requests.session()

    payload = {
     'password': password,
     'login': username,
     'redirect_uri': 'https://fantasy.premierleague.com/a/login',
     'app': 'plfpl-web'
    }

    login = 'https://users.premierleague.com/accounts/login/'

    responses = session.post(login, data=payload)
    
    return session.get(urlResponseToReturn,  auth=HTTPBasicAuth(username, password))

# Generates the ID's for the top fantasy teams in the world for the number specified by the users up to 50
def generateTeamIdsForTopPlayers(numberOfTeamsToPull, username, password):
    JSON = Teams.loginToSecureURL('https://fantasy.premierleague.com/api/leagues-classic/314/standings/', username, password)
    Data = JSON.json()
    Dumps = json.dumps(Data)
    readableData = json.loads(Dumps)
    x = 1
    teamIDs = dict()
    for currentTeamResults in readableData['standings']['results']:
        if x <= numberOfTeamsToPull:
            teamName = currentTeamResults['entry_name']
            id = currentTeamResults['entry']
            teamIDs[teamName] = id

        else:
            break

        x += 1

    return teamIDs
    
# Pull the data for a single users fantasy team
def getTeamDetails(teamID, username, password):
    gameweekNumber = genericMethods.generateCurrentGameweek()
    url = f'https://fantasy.premierleague.com/api/entry/{teamID}/event/{gameweekNumber}/picks/'
    Response = Teams.loginToSecureURL(url, username, password)  
    Data = Response.json()
    Dumps = json.dumps(Data)
    readableData = json.loads(Dumps)
    return readableData

# Returns all team names ask keys, with their associated team ID's
def teamNamesAsKeysAndIDsAsData():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for elements in readable:
        for keys in readable['teams']:
           id = keys['id']
           name = str.lower(keys['name'])
           teams[name] = id
    return teams

# Returns all team ids ask keys, with their associated team names
def teamIDsAsKeysAndNamesAsData():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for elements in readable:
        for keys in readable['teams']:
           id = str.lower(keys['name'])
           name = keys['id']
           teams[name] = id
    return teams

# Returns all team ids ask keys, with their historic gameweek difficulty as a comma seperated list for each team
def teamIDsAsKeysAndGameweekDifficultyAsList(startGameweek, endGameweek):
    urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
    teamsPlayingInCurrentPeriod =  Teams.allTeamsPlayingForAGameweek(startGameweek, endGameweek)
    teams = dict()
    for teamID in teamsPlayingInCurrentPeriod:
        difficultyOfUpcomingGamesForTeam = list()
        currentGameweek = startGameweek
        while currentGameweek <= endGameweek:
            teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(currentGameweek, currentGameweek)
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={currentGameweek}')
            for gameweekData in currentDumps:
                    if gameweekData['team_a'] == teamID:
                        difficultyOfUpcomingGamesForTeam.append(int(gameweekData['team_a_difficulty']))
                        currentGameweek += 1
                        break
                    if gameweekData['team_h'] == teamID:
                        difficultyOfUpcomingGamesForTeam.append(int(gameweekData['team_h_difficulty']))
                        currentGameweek += 1
                        break
            else:
                currentGameweek += 1

        teams[teamID] = difficultyOfUpcomingGamesForTeam

    return teams

# Returns all team ids ask keys, with their associated players as a comma seperated list for each team
def teamIDsAsKeysAndPlayerIDsAsList():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for elements in readable:
        for keys in readable['teams']:
           id = keys['id']
           playerIDs = list()
           for players in readable['elements']:
               if players['team'] == id:
                   playerIDs.append(players['id'])
           teams[id] = playerIDs

    return teams

# Print current data for team to console
def printTeamDataToConsole(teamID):
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for elements in readable:
        for keys in readable['teams']:
            teamName = keys['name']
            if keys['id'] == teamID:
                print('================================')
                print(f'Team: {teamName}')
                print('--------------------------------')
                for currentKey in keys:
                    currentValue = keys[currentKey]
                    print(f'{currentKey}: {currentValue}')
            if keys['id'] == teamID:
                net_strength_home = keys["strength_attack_home"] - keys["strength_defence_home"]
                net_strength_away = keys["strength_attack_away"] - keys["strength_defence_away"]
                print(f'net_strength_away: {net_strength_away}')
                print(f'net_strength_home: {net_strength_home}')
                print('================================')
                return

# Get all data for a gameweek for a team
# TODO: Finish this method off to print the data for a single team sensibly

def performanceSummaryForTeam(idOfTheTeamWeWantToLookAt):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        maxGameweek = genericMethods.generateCurrentGameweek() + 1
        currentGameweek = 1
        totalDict = dict()
        homeDict = dict()
        awayDict = dict()
        while currentGameweek <= maxGameweek:
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={currentGameweek}')
            for gameweekData in currentDumps:
                if gameweekData['team_h'] == teamID:
                    for data in gameweekData:
                        if data == 'stats':
                            for gameweekStats in gameweekData[data]:
                                dataToAddToList = dict()
                                for stat in gameweekStats['h']:
                                    currentStat = gameweekStats['identifier']
                                    currentPlayer = stat['element']
                                    dataToAddToList[currentPlayer] = stat['value']
                                awayDict[currentStat] = dataToAddToList
                        else:
                            homeDict[data] = gameweekData[data]
                    homeDict['was_away'] = False
                    homeDict['was_home'] = True
                    totalDict[currentGameweek] = homeDict

                if gameweekData['team_a'] == teamID:
                    for data in gameweekData:
                        if data == 'stats':
                            for gameweekStats in gameweekData[data]:
                                dataToAddToList = dict()
                                for stat in gameweekStats['a']:
                                    currentStat = gameweekStats['identifier']
                                    currentPlayer = stat['element']
                                    dataToAddToList[currentPlayer] = stat['value']
                                homeDict[currentStat] = dataToAddToList

                        else:
                            awayDict[data] = gameweekData[data]
                    awayDict['was_away'] = True
                    awayDict['was_home'] = False
                    totalDict[currentGameweek] = awayDict
            
            currentGameweek += 1

        return totalDict

# input is a team ID & the output is the game stats for last week for that team
def generateGameweekStats(idOfTheTeamWeWantToLookAt):
    lastGameweek = genericMethods.generateCurrentGameweek() - 1
    teamID = idOfTheTeamWeWantToLookAt
    urlBase = f'https://fantasy.premierleague.com/api/fixtures/?event={lastGameweek}'
    gameweekDumps = genericMethods.generateJSONDumpsReadable(urlBase)
    gameweekData = dict()
    for dumps in gameweekDumps:
            if teamID == dumps['team_a'] or teamID == dumps['team_h']:
                for stats in dumps['stats']:
                    currentIdentifier = stats['identifier']
                    gameweekData[currentIdentifier] = stats

    #TODO: TEST
    return gameweekData

# A method to pull the upcoming (N) gameweek difficulty for a particular team

def upcomingGameDifficultyListed(numberOfGameweeksToPullDataFor, idOfTheTeamWeWantToLookAt):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        currentGameweek = genericMethods.generateCurrentGameweek() + 1
        maxGameweek = currentGameweek + (numberOfGameweeksToPullDataFor - 1)
        difficultyOfUpcomingGamesForTeam = list()
        while currentGameweek <= maxGameweek:
            teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(currentGameweek, currentGameweek)
            if teamID in teamsPlayingInCurrentPeriod:
                currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={currentGameweek}')
                for gameweekData in currentDumps:
                        if gameweekData['team_a'] == teamID:
                            difficultyOfUpcomingGamesForTeam.append(int(gameweekData['team_a_difficulty']))
                            currentGameweek += 1
                            break
                        if gameweekData['team_h'] == teamID:
                            difficultyOfUpcomingGamesForTeam.append(int(gameweekData['team_h_difficulty']))
                            currentGameweek += 1
                            break
            else:
                currentGameweek += 1

        return difficultyOfUpcomingGamesForTeam

# List the ID's of any team that has played in a given period

def allTeamsPlayingForAGameweek(gameweekNumber, maxGameweekNumber):
     urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
     teamsPlayed = list()
     while gameweekNumber <= maxGameweekNumber:
         currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweekNumber}')
         for match in currentDumps:
             teamsPlayed.append(match['team_a'])
             teamsPlayed.append(match['team_h'])
             gameweekNumber += 1
    
     return teamsPlayed

# Generate list of playerID's and names for a given team
def generateListOfPlayerIDsAsKeysForTeam(teamID):
    playerIDMatchList = dict()
    gameweekSummarySub = "bootstrap-static/"
    url = genericMethods.mergeURL(gameweekSummarySub)
    gameweekSummaryDataReadable = genericMethods.generateJSONDumpsReadable(url)

    for y in gameweekSummaryDataReadable['elements']:
        dumpsY = json.dumps(y)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            if formattedY['team'] == teamID:
                firstName = formattedY['first_name']
                secondName = formattedY['second_name']
                fullName = f'{firstName} {secondName}'
                cleanedFullName = str.lower(genericMethods.unicodeReplace(fullName))
                id = formattedY['id']
                playerIDMatchList[id] = cleanedFullName

    return playerIDMatchList

# A method to pull the average goals conceeded by gameweek difficulty for a particular team

def goalsConceededByDifficulty(idOfTheTeamWeWantToLookAt, gameweek):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        maxGameweek = gameweek
        gameweek = 1
        difficulty2 = list()
        difficulty3 = list()
        difficulty4 = list()
        difficulty5 = list()
        difficultyOfGamesWithGoalsConceededListed = dict()
        while gameweek <= maxGameweek:
            teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(gameweek, gameweek)
            if teamID in teamsPlayingInCurrentPeriod:
                currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweek}')
                for gameweekData in currentDumps:
                        if gameweekData['team_a'] == teamID:
                            if gameweekData['team_h_score'] != None:
                                if gameweekData['team_h_score'] <= 5:
                                    gameweekDifficulty = gameweekData['team_a_difficulty']
                                    if gameweekDifficulty == 2:
                                            difficulty2.append(gameweekData['team_h_score'])
                                    if gameweekDifficulty == 3:
                                            difficulty3.append(gameweekData['team_h_score'])
                                    if gameweekDifficulty == 4:
                                            difficulty4.append(gameweekData['team_h_score'])
                                    if gameweekDifficulty == 5:
                                            difficulty5.append(gameweekData['team_h_score'])
                            gameweek += 1
                        if gameweekData['team_h'] == teamID:
                            if gameweekData['team_a_score'] != None:
                                if gameweekData['team_a_score'] <= 5:
                                    gameweekDifficulty = gameweekData['team_h_difficulty']
                                    if gameweekDifficulty == 2:
                                            difficulty2.append(gameweekData['team_a_score'])
                                    if gameweekDifficulty == 3:
                                            difficulty3.append(gameweekData['team_a_score'])
                                    if gameweekDifficulty == 4:
                                            difficulty4.append(gameweekData['team_a_score'])
                                    if gameweekDifficulty == 5:
                                            difficulty5.append(gameweekData['team_a_score'])
                            gameweek += 1
            else:
                gameweek += 1

        
        difficultyOfGamesWithGoalsConceededListed[2] = difficulty2
        difficultyOfGamesWithGoalsConceededListed[3] = difficulty3
        difficultyOfGamesWithGoalsConceededListed[4] = difficulty4
        difficultyOfGamesWithGoalsConceededListed[5] = difficulty5

        averageGoalsByDifficulty = dict()

        for difficulty in difficultyOfGamesWithGoalsConceededListed:
            if len(difficultyOfGamesWithGoalsConceededListed[difficulty]) != 0:
                averageGoalsConceeded = round(genericMethods.listAverage(difficultyOfGamesWithGoalsConceededListed[difficulty]) , 1)  
                averageGoalsByDifficulty[difficulty] = averageGoalsConceeded

        return averageGoalsByDifficulty

# A method to pull the average goals scored gameweek difficulty for a particular team

def goalsScoredByDifficulty(idOfTheTeamWeWantToLookAt, gameweek):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        maxGameweek = gameweek
        gameweek = 1
        difficulty2 = list()
        difficulty3 = list()
        difficulty4 = list()
        difficulty5 = list()
        difficultyOfGamesWithGoalsScoredListed = dict()
        while gameweek <= maxGameweek:
            teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(gameweek, gameweek)
            if teamID in teamsPlayingInCurrentPeriod:
                currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweek}')
                for gameweekData in currentDumps:
                        if gameweekData['team_a'] == teamID:
                            if gameweekData['team_a_score'] != None:
                                gameweekDifficulty = gameweekData['team_a_difficulty']
                                if gameweekDifficulty == 2:
                                        difficulty2.append(gameweekData['team_a_score'])
                                if gameweekDifficulty == 3:
                                        difficulty3.append(gameweekData['team_a_score'])
                                if gameweekDifficulty == 4:
                                        difficulty4.append(gameweekData['team_a_score'])
                                if gameweekDifficulty == 5:
                                        difficulty5.append(gameweekData['team_a_score'])
                            gameweek += 1
                        if gameweekData['team_h'] == teamID:
                            if gameweekData['team_h_score'] != None:
                                gameweekDifficulty = gameweekData['team_h_difficulty']
                                if gameweekDifficulty == 2:
                                        difficulty2.append(gameweekData['team_h_score'])
                                if gameweekDifficulty == 3:
                                        difficulty3.append(gameweekData['team_h_score'])
                                if gameweekDifficulty == 4:
                                        difficulty4.append(gameweekData['team_h_score'])
                                if gameweekDifficulty == 5:
                                        difficulty5.append(gameweekData['team_h_score'])
                            gameweek += 1
            else:
                gameweek += 1

        
        difficultyOfGamesWithGoalsScoredListed[2] = difficulty2
        difficultyOfGamesWithGoalsScoredListed[3] = difficulty3
        difficultyOfGamesWithGoalsScoredListed[4] = difficulty4
        difficultyOfGamesWithGoalsScoredListed[5] = difficulty5

        averageGoalsByDifficulty = dict()

        for difficulty in difficultyOfGamesWithGoalsScoredListed:
            if len(difficultyOfGamesWithGoalsScoredListed[difficulty]) != 0:
                averageGoalsScored = round(genericMethods.listAverage(difficultyOfGamesWithGoalsScoredListed[difficulty]) , 1)  
                averageGoalsByDifficulty[difficulty] = averageGoalsScored

        return averageGoalsByDifficulty

# A method to pulling the upcoming gameweek difficulty for a particular team

def nextGameDifficulty(idOfTheTeamWeWantToLookAt, gameweek):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(gameweek, gameweek)
        if teamID in teamsPlayingInCurrentPeriod:
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweek}')
            for gameweekData in currentDumps:
                    if gameweekData['team_a'] == teamID:
                        return gameweekData['team_a_difficulty']
                    if gameweekData['team_h'] == teamID:
                        return gameweekData['team_h_difficulty']
        else:
                return None

# Combined method for pulling the upcoming likelihoood for a team to score for all teams

def generateLikelihoodToScoreByTeamForNextGame(gameweek):
    teamIDsAndNames = Teams.teamIDsAsKeysAndNamesAsData()
    teamDifficultyReference = dict()
    nextGameDifficultyByTeam = dict()
    length = len(teamIDsAndNames) - 1

    for teamID in teamIDsAndNames:
        teamName = teamIDsAndNames[teamID]
        teamDifficultyReference[teamID] = Teams.goalsScoredByDifficulty(teamID, gameweek)
        nextGameDifficultyByTeam[teamID] = Teams.nextGameDifficulty(teamID, gameweek)

        currentIndex = list(teamIDsAndNames.keys()).index(teamID)
        genericMethods.runPercentage(length, currentIndex, "Gathering team difficulty and goals scored index", "Complete: Gathered team difficulty and goals scored index")

    print("")
    nextGameLikelihoodtoConceed = dict()

    for teamID in nextGameDifficultyByTeam:
        teamName = teamIDsAndNames[teamID].capitalize()
        upcomingDifficulty = nextGameDifficultyByTeam[teamID]
        try:
            activeTeamReference = teamDifficultyReference[teamID]
            avgGoals = activeTeamReference[upcomingDifficulty]
        except:
            avgGoals = "N/A"

        nextGameLikelihoodtoConceed[teamName] = avgGoals
                                                        
        currentIndex = list(teamIDsAndNames.keys()).index(teamID)
        genericMethods.runPercentage(length, currentIndex, "Gathering upcoming difficulty by team", "Complete: Gathered upcoming difficulty by team")

    print("")

    return nextGameLikelihoodtoConceed

# Combined method for pulling the upcoming likelihoood for a team to conceed for all teams

def generateLikelihoodToConceedByTeamForNextGame(gameweek):
    teamIDsAndNames = Teams.teamIDsAsKeysAndNamesAsData()
    teamDifficultyReference = dict()
    nextGameDifficultyByTeam = dict()
    length = len(teamIDsAndNames) - 1

    for teamID in teamIDsAndNames:
        teamName = teamIDsAndNames[teamID]
        teamDifficultyReference[teamID] = Teams.goalsConceededByDifficulty(teamID, gameweek)
        nextGameDifficultyByTeam[teamID] = Teams.nextGameDifficulty(teamID, gameweek)

        currentIndex = list(teamIDsAndNames.keys()).index(teamID)
        genericMethods.runPercentage(length, currentIndex, "Gathering team difficulty and goals conceeded index", "Complete: Gathered team difficulty and goals conceeded index")

    nextGameLikelihoodtoConceed = dict()
    print("")

    for teamID in nextGameDifficultyByTeam:
        teamName = teamIDsAndNames[teamID].capitalize()
        upcomingDifficulty = nextGameDifficultyByTeam[teamID]
        try:
            activeTeamReference = teamDifficultyReference[teamID]
            avgGoals = activeTeamReference[upcomingDifficulty]
        except:
            avgGoals = "N/A"

        nextGameLikelihoodtoConceed[teamName] = avgGoals
                                                        
        currentIndex = list(teamIDsAndNames.keys()).index(teamID)
        genericMethods.runPercentage(length, currentIndex, "Gathering upcoming difficulty by team", "Complete: Gathered upcoming difficulty by team")

    print("")

    return nextGameLikelihoodtoConceed

# Generate list of fixtures

def fixturesForGameweekByTeamID(gameweek):
    urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
    currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweek}')
    fixtureData = dict()
    for gameweekData in currentDumps:
        homeTeam = gameweekData['team_h']
        awayTeam = gameweekData['team_a']
        fixtureData[homeTeam] = awayTeam

    return fixtureData

# A method to pull the results for a gameweek

def resultsForGameweek(gameweek):
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        results = dict()
        teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(gameweek, gameweek)
        currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweek}')
        for gameweekData in currentDumps:
            homeTeam = gameweekData['team_h']
            homeResult = gameweekData['team_h_score']
            awayTeam = gameweekData['team_a']
            awayResult = gameweekData['team_a_score']

            results[homeTeam] = homeResult
            results[awayTeam] = awayResult

        return results

# A method to pull the fixtures for a gameweek

def fixturesForGameweek(gameweek):
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        fixtures = dict()
        teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(gameweek, gameweek)
        currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweek}')
        for gameweekData in currentDumps:
            homeTeam = gameweekData['team_h']
            awayTeam = gameweekData['team_a']

            fixtures[homeTeam] = awayTeam

        return fixtures

# Returns all team ID's as keys, with their associated home and away strength

def strengthHomeAndAwayByTeam():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for elements in readable:
        for keys in readable['teams']:
           strength = dict()
           id = keys['id']
           awayStrength = keys['strength_overall_away']
           homeStrength = keys['strength_overall_home']
           strength['home'] = homeStrength
           strength['away'] = awayStrength
           teams[id] = strength

    return teams
