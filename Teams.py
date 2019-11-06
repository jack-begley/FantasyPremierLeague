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
    gameweekNumber = generateCurrentGameweek()
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
           id = keys['code']
           name = str.lower(keys['name'])
           teams[name] = id
    return teams

# Returns all team ids ask keys, with their associated team names
def teamNamesAsKeysAndIDsAsData():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for elements in readable:
        for keys in readable['teams']:
           id = keys['name']
           name = str.lower(keys['code'])
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
            if keys['code'] == teamID:
                print('================================')
                print(f'Team: {teamName}')
                print('--------------------------------')
                for currentKey in keys:
                    currentValue = keys[currentKey]
                    print(f'{currentKey}: {currentValue}')
    print('================================')

# Generate static data for team performance
def generateDataForTeam(teamID):
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for elements in readable:
        for keys in readable['teams']:
            if keys['code'] == teamID:
                teams[keys] = readable[keys]

    teams['net_strength_home'] = teams["strength_attack_home"] - teams["strength_defence_home"]
    teams['net_strength_away'] = teams["strength_attack_away"] - teams["strength_defence_away"]

    return teams


# Get all data for a gameweek for a team
def performanceSummaryForTeam(idOfTheTeamWeWantToLookAt):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        maxGameweek = genericMethods.generateCurrentGameweek()
        currentGameweek = 1
        homeDict = dict()
        awayDict = dict()
        homeDict = []
        awayDict = []
        while currentGameweek <= maxGameweek:
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={currentGameweek}')
            for gameweekData in currentDumps:
                if gameweekData['team_h'] == teamID:
                    for key in gameweekData:
                        currentData = gameweekData[key]
                        if not homeDict:
                            homeDict[key] = homeDict[key],gameweekData[key]
                        else:
                            homeDict[key] = gameweekData[key]
                if gameweekData['team_a'] == teamID:
                        currentData = gameweekData[key]                        
                        if not awayDict:
                            awayDict[key] = awayDict[key],gameweekData[key]
                        else:
                            awayDict[key] = gameweekData[key]

            currentGameweek += 1

        totalDict['away_performance'] = awayDict
        totalDict['home_performance'] = homeDict

        return totalDict