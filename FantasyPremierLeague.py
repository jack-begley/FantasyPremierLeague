

from pprint import pprint
import requests
import json
import argparse
import csv 
import zipfile
import pyodbc
import aiohttp
import asyncio
import urllib.request
import urllib.parse

#Setting up url construction

def mergeURL(sub):
    return 'https://fantasy.premierleague.com/api/' + sub;
# Syntax e.g. = print(mergeURL(userSummary))

# URL set up and league codes
from datetime import date
today = date.today()

"""
The FPL module.

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
"""

coreApi = 'https://fantasy.premierleague.com/api/'
playerSummary = "element-summary/"
# User summary = summary of the  player where the number on the end is the player ID: https://fantasy.premierleague.com/api/element-summary/301/
email = "jack.bgl@googlemail.com"
classicStandings = "leagues-classic-standings/"
h2hStandings = "leagues-h2h-standings/"
teams = "entry/"
playersSub = "bootstrap-static/"
subLog = "Athomeaa"
playersInfoSub = "allPlayersInfo.json"
myTeamString = "2923192/1/live"
myTeam = 2923192

players = mergeURL(playersSub)
playersInfo = mergeURL(playersInfoSub)
userTeam = mergeURL(teams)+myTeamString

# League Codes:

tygwyn = 'wo7rlj'
brooks = 'sgvzsa'
savanta = 'op3f9m'
mrsbaines = 'yanfqi'

tygwynID = 856255
brooksID = 699088
savantaID = 806190
mrsbainesID = 1164443

# Export Names:

datatype = ""
exportName = (f"FPL Raw {datatype} data - {today}.csv")
exportName_JSON = (f"FPL {datatype} Raw data - {today}.json")


# Testing fpl import package

from fpl import FPL

playersJSON = requests.get(url=players)
playersData = playersJSON.json()
playersDataDumps = json.dumps(playersData)
# playersDataPrePrep = playersData.read()
playersDataReadable = json.loads(playersDataDumps)
datatype = "Player"

#with open(exportName_JSON, "w") as outfile:
#    json.dump(playersData, outfile)

# Print everything from the players object 
for x in playersDataReadable:
    dumpsX = json.dumps(x)
    readableX = json.loads(dumpsX)
    test = playersDataReadable[x]
    if isinstance(test, int) == False:
        print(x + ":")
        for y in playersDataReadable[x]:
            dumpsY = json.dumps(y)
            if isinstance(y,dict):
                formattedY = json.loads(dumpsY)
                for z in formattedY:
                    print("%s: %s" % (z, formattedY[z]))
            else:
                print("%s: %s" % (y, playersDataReadable[x][y]))
    else:
         print("%s: %s" % (x, playersDataReadable[x]))

    print("")
