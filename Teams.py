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
    
def getTeamDetails(teamID, username, password):
    gameweekNumber = (math.floor((datetime.datetime.now() - datetime.datetime(2019, 8, 5)).days/7)) - 2
    url = f'https://fantasy.premierleague.com/api/entry/{teamID}/event/{gameweekNumber}/picks/'
    Response = loginToSecureURL(url, username, password)  
    Data = Response.json()
    Dumps = json.dumps(Data)
    readableData = json.loads(Dumps)
    return readableData