

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
classicStandings = "leagues-classic-standings/"
h2hStandings = "leagues-h2h-standings/"
teams = "entry/"
playersSub = "bootstrap-static/"
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

# Try and parse text as an int. Returns integer or text

def parse(userInput):
    try:
        return int(userInput)
    except ValueError:
       return str(userInput)

# Try and parse and int. Results in boolean outputs
def isInt(userInput):
    try: 
        int(userInput)
        return True
    except ValueError:
        return False

# Quit the program if the user decides they want to leave
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

# Print all of the player data in the console
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

# Getting the information of a player based on their surname
def playerInfoBySurname(playerSurname):

    url = mergeURL(playersSub)
    playersJSON = requests.get(url)
    playersData = playersJSON.json()
    playersDataDumps = json.dumps(playersData)
    playersDataReadable = json.loads(playersDataDumps)

    for y in playersDataReadable['elements']:
        dumpsY = json.dumps(y)
        playerInApi = False
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
                playerInApi = True
                break

        elif playerSurname == "":
                print("")
                print("============================================================================")
                print("!! ERROR: No input won't work - you need a players surname:")
                print("============================================================================")
                playerSurname = str.lower(input("Try again:"))
                playerInfoBySurname(playerSurname)

    if playerInApi == False:
        print("")
        print("===============================================================")
        print("!! ERROR:Player not found - please check spelling and try again:")
        print("===============================================================")
        print("")
        playerInApi = True
        playerSurname = str.lower(input("Try again:"))
        playerInfoBySurname(playerSurname)

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
    print("------------------------------------------------------------------------------")
    print("")
    print("What would you like to see?:")
    userInput = input(">")
    print("")
    parse(userInput)
    if isInt(userInput) == True:
        userInputInt = int(userInput)
        if userInputInt ==  1:
            playerRoutine()

        else:            
            print("====================================================================================")
            print("!! ERROR:Command not recognised - please pick one of the above options and try again:")
            print("====================================================================================")
            print("")
            introRoutine()

    elif userInput == "game week summary":
        printAllData(playersSub, "playersSub")

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
                print(" [1] All players")
                print(" [2] A player (by surname)")
                print(" [3] A comma seperated list of playes (by surname)")
                print(" [4] A player (by player ID)")
                print(" [5] All players ID's printed")
                print("------------------------------------------------------------------------")
                print("")
                print("What would you like to see?:")
                playerUserInputInitial = input(">")
                print("")
                parse(playerUserInputInitial)

                if isInt(playerUserInputInitial) == True:
                    playerUserInputInitialInt = int(playerUserInputInitial)
                    if playerUserInputInitialInt == 1:
                        print("")
                        printAllData(playersSub, playersFileName)

                    elif playerUserInputInitialInt == 2:
                        print("----------------------------------")
                        print("Let us know who you're looking for:")
                        print("!! TYPE IN A SURNAME")
                        print("----------------------------------")
                        playerSurname = str.lower(input(">"))
                        playerInfoBySurname(playerSurname)
                        endRoutine()
                    
                    elif playerUserInputInitialInt == 3:
                        print("-----------------------------------------------------------------------------------------------------")
                        print("Let us know who you're looking for in the format \"surname,surname,surname\" e.g. salah,sterling,kane:")
                        print("!! TYPE IN THE SURNAMES")
                        print("-----------------------------------------------------------------------------------------------------")
                        playerSurnameList = str.lower(input(">"))
                        playerListNew = list()
                        playerList = list()
                        playerListNew = playerSurnameList.split(",")
                        for i in playerListNew:
                            j = i.replace(' ', '')
                            playerList.append(j)
                        for playerSurname in playerList:
                            playerInfoBySurname(playerSurname)
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
print("V.0.0.002")
print("")
print("==============================")
print("")
print("Welcome to the FPL console app for data extraction.")
print("")

introRoutine()