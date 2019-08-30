

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
datatype = "Player"

with open(exportName_JSON, "w") as outfile:
    json.dump(playersData, outfile)

# =======================

teamJSON = requests.get(url=userTeam)
teamData = teamJSON.json()
datatype = "Team"

with open(exportName_JSON, "w") as outfile:
    json.dump(teamData, outfile)

# =======================

from colorama import Fore, init
from prettytable import PrettyTable

async def my_team(user_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login("jack.bgl@googlemail.com", subLog)
        user = await fpl.get_user(user_id)
        team = await user.get_team()
    print(team)

asyncio.run(my_team(myTeam))



async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        fdr = await fpl.FDR()
    fdr_table = PrettyTable()
    fdr_table.field_names = [
        "Team", "All (H)", "All (A)", "GK (H)", "GK (A)", "DEF (H)", "DEF (A)",
        "MID (H)", "MID (A)", "FWD (H)", "FWD (A)"]
    for team, positions in fdr.items():
        row = [team]
        for difficulties in positions.values():
            for location in ["H", "A"]:
                if difficulties[location] == 5.0:
                    row.append(Fore.RED + "5.0" + Fore.RESET)
                elif difficulties[location] == 1.0:
                    row.append(Fore.GREEN + "1.0" + Fore.RESET)
                else:
                    row.append(f"{difficulties[location]:.2f}")
        
            fdr_table.add_row(row)
    fdr_table.align["Team"] = "l"
    print(fdr_table)
    
if __name__ == '__main__':
    asyncio.run(main())

# About My Team


# Return JSON for players sub


# Write the data into a CSV
# newDoc = csv.writer(open(exportName, "wb+"))

# for item in playersData:
#     newDoc.writerow([
#         item["events"],
#         item["game_settings"],
#         ])

# PRINT new data

#for key, value in playersData.items():
#        for events in key[0]:
#                pprint(events)
#        for settings in key[1]:
#                pprint(settings)

# Getting the keys

for key, value in playersData.items():
        pprint("Key:")
        pprint(key)