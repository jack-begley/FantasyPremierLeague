from gameweekSummary import *
from playerData import *
from genericMethods import *

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

        sys.exit(0)

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

        if userInputInt ==  3:
            gameweekRoutine()

        else:            
            print("====================================================================================")
            print("!! ERROR:Command not recognised - please pick one of the above options and try again:")
            print("====================================================================================")
            print("")
            introRoutine()

    elif userInput == "game week summary":
        printAllData(gameweekSummarySub, "playersSub")

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
                print("")
                print(" Data Exports: ")
                print(" [4] All player data for all gameweeks (to excel)")
                print("")
                print(" TEST:")
                print(" [99] Test: all player ID's and generating the correlcoef")
                print("------------------------------------------------------------------------")
                print("")
                print("What would you like to see?:")
                playerUserInputInitial = input(">")
                print("")
                parse(playerUserInputInitial)

                if isInt(playerUserInputInitial) == True:
                    playerUserInputInitialInt = int(playerUserInputInitial)
                    if playerUserInputInitialInt == 1:
                        print("-----------------------------------")
                        print("Let us know who you're looking for:")
                        print("!! TYPE IN A SURNAME")
                        print("-----------------------------------")
                        playerSurname = str.lower(input("> "))
                        playerInfoBySurname(playerSurname)
                        endRoutine()

                    if playerUserInputInitialInt == 2:
                        print("-----------------------------------")
                        print("Let us know who you're looking for:")
                        print("!! TYPE IN A SURNAME")
                        print("-----------------------------------")
                        playerSurname = str.lower(input("> "))
                        playerData = allPlayerDataBySurname(playerSurname)
                        print("")
                        print("-----------------------------------")
                        print("Would you like to export the data?:")
                        print("!! TYPE IN Y/N")
                        print("-----------------------------------")
                        userInput = str.lower(input("> "))
                        if userInput == 'y':
                            gameweekHeaders = generateCommaSeperatedGameweekNumberList()
                            printListToExcel(playerData, gameweekHeaders)
                        else:
                            endRoutine()

                    elif playerUserInputInitialInt == 3:
                        print("-------------------------------------------")
                        print("Let us know what week you're interested in:")
                        print("!! TYPE IN A GAMEWEEK NUMBER")
                        print("-------------------------------------------")
                        gameweekNumber = str.lower(input("> "))
                        playerInfoByGameweek(gameweekNumber)
                        endRoutine()

                    elif playerUserInputInitialInt == 4:
                        playerIDs = generatePlayerIDs()
                        exportPlayerDataByGameweek(playerIDs)

                    elif playerUserInputInitialInt == 99:
                        elementsList = gatherHistoricalPlayerData()
                        allData = convertStringDictToInt(elementsList, "allData")
                        correl = correlcoeffGeneration(allData,'total_points')

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

# Player specific section of the program. Contains the menu items for the player part of the console app
def gameweekRoutine():
                print("------------------------------------------------------------------------")
                print("You've said you want to take a look at the gameweek data. You can look at:")
                print("!! PLEASE SELECT A NUMBER")
                print("------------------------------------------------------------------------")
                print(" [1] All players printed in console")
                print(" [2] A player (by surname)")
                print(" [3] A comma seperated list of playes (by surname)")
                print("------------------------------------------------------------------------")
                print(" [99] Print all player data to console")
                print(" [101] Export all player data to excel")
                print("------------------------------------------------------------------------")
                print("")
                print("What would you like to see?:")
                playerUserInputInitial = input(">")
                print("")
                parse(playerUserInputInitial)

                if isInt(playerUserInputInitial) == True:
                    playerUserInputInitialInt = int(playerUserInputInitial)
                    if playerUserInputInitialInt == 1:
                        generatePlayersFullNameList()
                        print("------------------------------------")
                        print("How would you like to see the output?")
                        print("------------------------------------")
                        print(" [1] Full list")
                        print(" [2] Comma seperated list  of surnames")
                        print("------------------------------------")
                        playerListInput = input(" > ")
                        # try and put the input in as an integer
                        parse(playerListInput)
                        if isInt(playerListInput):
                            if int(playerListInput) == 1:
                                for player in gameweekSummaryListFull:
                                    print(player)
                            elif int(playerListInput) == 2:
                                gameweekSummaryListCleaned = str(gameweekSummaryListSecond).replace("'","").replace("[","").replace("]","")
                                print(gameweekSummaryListCleaned)
                                copyTo = Tk()
                                copyTo.clipboard_clear()
                                copyTo.clipboard_append(gameweekSummaryListCleaned)
                                copyTo.update()
                                copyTo.destroy()
                                print("")
                                print("// This has been copied to your clipboard.")
                                print("")
                                return
                            else:
                                print("======================================================================================")
                                print("!! ERROR:Command wasn't recognised- please pick one of the above options and try again:")
                                print("======================================================================================")
                                print("")
                                generatePlayersFullNameList()

                        else:
                            print("====================================================================================")
                            print("!! ERROR:Input was not a number - please pick one of the above options and try again:")
                            print("====================================================================================")
                            print("")
                            generatePlayersFullNameList()


                    elif playerUserInputInitialInt == 2:
                        print("----------------------------------")
                        print("Let us know who you're looking for:")
                        print("!! TYPE IN A SURNAME")
                        print("----------------------------------")
                        playerSurname = str.lower(input("> "))
                        playerInfoBySurname(playerSurname)
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
                            playerInfoBySurname(playerSurname)
                        endRoutine()

                    elif playerUserInputInitialInt == 99:
                        printAllData(gameweekSummarySub, playersFileName)

                    elif playerUserInputInitialInt == 101:
                        exportToExcelPlayers()
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
print("V.0.0.210")
print("")
print("==============================")
print("")
print("Welcome to the FPL console app for data extraction.")
print("")

introRoutine()
