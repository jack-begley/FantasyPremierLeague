

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
email = "jack.bgl@googlemail.com"
classicStandings = "leagues-classic-standings/"
h2hStandings = "leagues-h2h-standings/"
teams = "entry/"
playersSub = "bootstrap-static/"
subLog = "Athomeaa"
playersInfoSub = "allPlayersInfo.json"
myTeamString = "2923192/1/live"
myTeam = 2923192
userInput = ""

playersURL = mergeURL(playersSub)
playersFileName = "players"
# playersInfo = mergeURL(playersInfoSub)
# userTeam = mergeURL(teams)+myTeamString

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

#with open(exportName_JSON, "w") as outfile:
#    json.dump(playersData, outfile)

# Print everything from the players object 

def isInt(userInput):
    try: 
        int(userInput)
        return True
    except ValueError:
        return False

def endRoutine():
    print("// Would you like to run another function?")
    print("Y/N:")

    finalDecision = str.lower(input(">"))

    if finalDecision == "y":
        print("------------------------------------------------------")
        print("")
        introRoutine()
    else:
        quit()

def printAllData(urlAddOn, fileName):

    url = mergeURL(urlAddOn)

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

def playerInfoBySurname(playerSurname):

    url = mergeURL(playersSub)
    playersJSON = requests.get(url)
    playersData = playersJSON.json()
    playersDataDumps = json.dumps(playersData)
    playersDataReadable = json.loads(playersDataDumps)

    for y in playersDataReadable['elements']:
        dumpsY = json.dumps(y)
        if isinstance(y,dict):
            formattedY = json.loads(dumpsY)
            if str.lower(formattedY["second_name"]) == playerSurname:
                
                # Create format for printing the title
                firstName = formattedY["first_name"]
                secondName = formattedY["second_name"]
                playerSummaryTitle = f"// Player summary: {firstName} {secondName}"
                underline = "-" * len(playerSummaryTitle)

                # Print the data with the title
                print("")
                print(underline)
                print(playerSummaryTitle)
                print(underline)
                print("Total points: " + str(formattedY["total_points"]))
                print("Transfers in: " + str(formattedY["transfers_in"]))
                print("Transfers out: " + str(formattedY["transfers_out"]))
                print("// Net Transfers: " + str(int(formattedY["transfers_in"] - formattedY["transfers_out"])))
                print("Transfers in for gameweek: " + str(formattedY["transfers_in_event"]))
                print("Transfers out for gameweek: " + str(formattedY["transfers_out_event"]))
                print("// Net Transfers for gameweek: " + str(int(formattedY["transfers_in_event"] - formattedY["transfers_out_event"])))
                print("")
                break

        elif playerSurname == "":
                print("============================================================================")
                print("!! ERROR: No input won't work - you need a players surname, please try again:")
                print("============================================================================")
                playerSurname = str.lower(input(">"))
                playerInfoBySurname(playerSurname)

        else:
            print("===============================================================")
            print("!! ERROR:Player not found - please check spelling and try again:")
            print("===============================================================")
            playerSurname = str.lower(input(">"))
            playerInfoBySurname(playerSurname)

    endRoutine()

print("==============================")
print(" ________  _______  _____")
print("|_   __  ||_   __ \|_   _|")
print("  | |_ \_|  | |__) | | |")  
print("  |  _|     |  ___/  | |   _")  
print(" _| |_     _| |_    _| |__/ |") 
print("|_____|   |_____|  |________|")
print("")
print("==============================")
print("")
print("Welcome to the FPL console app for data extraction.")
print("")

def playerRoutine():
                print("You've said you want to take a look at the player data. You can look at:")
                print("// PLEASE SELECT A NUMBER")
                print(" [1] All players")
                print(" [2] A player (by surname)")
                print(" [3] A player (by player ID)")
                print(" [4] All players ID's printed:")
                print("")
                print("What would you like to see?:")
                playerUserInputInitial = int(input(">"))

                if isInt(playerUserInputInitial) == True:
                    if playerUserInputInitial == 1:
                        print("")
                        printAllData(playersSub, playersFileName)
                    elif playerUserInputInitial == 2:
                        print("")
                        print("------------------------------------------------------")
                        print("Let us know who you're looking for:")
                        print("// TYPE IN A SURNAME")
                        print("------------------------------------------------------")
                        print("")
                        playerSurname = str.lower(input(">"))
                        playerInfoBySurname(playerSurname)
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

def introRoutine():
    print("To access the different areas of the data type below what you want to see from:")
    print("// PLEASE SELECT A NUMBER")
    print(" [1] Players")
    print(" [2] Teams")
    print(" [3] Game week summary")
    print(" [4] My league performance")
    print("")
    print("What would you like to see?:")
    userInput = int(input(">"))
    if isInt(userInput) == True:
        if userInput ==  1:
            playerRoutine()

        else:
            print("====================================================================================")
            print("!! ERROR:Input was not a number - please pick one of the above options and try again:")
            print("====================================================================================")
            print("")
            introRoutine()

    elif userInput == "game week summary":
        printAllData(playersSub, "playersSub")

        #TODO: Test all active URLs, Repair "Teams" URL
        # printAllData(teams, "team")

    else:
        print("==============================================================================================================")
        print("!! ERROR:Your command hasn't been recognised, try again with one of the options above, or exit the application.")
        print("==============================================================================================================")
        print("")
        print("")
        introRoutine()

introRoutine()