import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import requests
import genericMethods
import playerData
import gameweekSummary
from requests.auth import HTTPBasicAuth
from gameweekSummary import *
from playerData import *
from genericMethods import *



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
    JSON = loginToSecureURL('https://fantasy.premierleague.com/api/leagues-classic/314/standings/', username, password)
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
    Response = loginToSecureURL(url, username, password)  
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

# Generate static data for team performance
def generateDataForTeam(teamID):
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for elements in readable:
        for keys in readable['teams']:
            if keys['id'] == teamID:
                teams[keys] = readable[keys]

    teams['net_strength_home'] = teams["strength_attack_home"] - teams["strength_defence_home"]
    teams['net_strength_away'] = teams["strength_attack_away"] - teams["strength_defence_away"]

    return teams


# Get all data for a gameweek for a team

# TODO: Finish this method off to print the data for a single team sensibly

def performanceSummaryForTeam(idOfTheTeamWeWantToLookAt):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        maxGameweek = genericMethods.generateCurrentGameweek()
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

def upcomingGameDifficulty(numberOfGameweeksToPullDataFor, idOfTheTeamWeWantToLookAt):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        currentGameweek = genericMethods.generateCurrentGameweek() + 1
        maxGameweek = currentGameweek + (numberOfGameweeksToPullDataFor - 1)
        difficultyOfUpcomingGamesForTeam = list()
        while currentGameweek <= maxGameweek:
            teamsPlayingInCurrentPeriod = allTeamsPlayingForAGameweek(currentGameweek, currentGameweek)
            if teamID in teamsPlayingInCurrentPeriod:
                currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={currentGameweek}')
                for gameweekData in currentDumps:
                        if gameweekData['team_a'] == teamID:
                            difficultyOfUpcomingGamesForTeam.append(gameweekData['team_a_difficulty'])
                            currentGameweek += 1
                            break
                        if gameweekData['team_h'] == teamID:
                            difficultyOfUpcomingGamesForTeam.append(gameweekData['team_h_difficulty'])
                            currentGameweek += 1
                            break
            else:
                currentGameweek += 1

        averageDifficultyScore = round(((genericMethods.indexValue(genericMethods.listAverage(difficultyOfUpcomingGamesForTeam), 5, 2)) / 10) , 0)

        return averageDifficultyScore

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

 # Method for printing the 
def printDifficultyScores(indexedSetOfData):
    x = 1
    for data in indexedSetOfData:
        currentIndex = list(indexedSetOfData).index(data)
        if currentIndex <= 20:
            seperatedValues = str(data).split(',')
            cleanedName = str(seperatedValues[0]).replace('(', '').replace(')', '').replace(",", ': ').replace("'", '')
            cleanedData = int(round(float(seperatedValues[1].replace(')', '')),2))
            print(f'{cleanedName}: {cleanedData:,}/10')
        else:
            return