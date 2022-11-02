import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import requests
import json
import genericMethods
import playerData
import Teams
from requests.auth import HTTPBasicAuth



# Verifies Auth to allow users to activate URLs that require login
def loginToSecureURL(urlResponseToReturn, username, password):
    session = requests.session()

    url = 'https://users.premierleague.com/accounts/login/'

    headers = {
       'authority': 'users.premierleague.com' ,
       'cache-control': 'max-age=0' ,
       'upgrade-insecure-requests': '1' ,
       'origin': 'https://fantasy.premierleague.com' ,
       'content-type': 'application/x-www-form-urlencoded' ,
       'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' ,
       'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
       'sec-fetch-site': 'same-site' ,
       'sec-fetch-mode': 'navigate' ,
       'sec-fetch-user': '?1' ,
       'sec-fetch-dest': 'document' ,
       'referer': 'https://fantasy.premierleague.com/my-team' ,
       'accept-language': 'en-US,en;q=0.9,he;q=0.8' ,
    }

    payload = {
     'password': password,
     'login': username,
     'redirect_uri': 'https://fantasy.premierleague.com/a/login',
     'app': 'plfpl-web'
    }
    session.post(url, data=payload, headers = headers)

    return session.get(urlResponseToReturn)
    
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

# Generate the data for next fixture difficulty ranked
def gameweekDifficultyRankedForTeams(gw, numOfGameweeksInFuture):
        gwNow = genericMethods.generateCurrentGameweek()
        endGw = gw + numOfGameweeksInFuture
        fixtures = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/fixtures/?event={gwNow}')
        if len(fixtures) < 10:
            fixtures = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/fixtures/?event={gwNow-1}')
        scores = dict()
        leaderboard = dict()
        length = len(fixtures)
        current = 1
        for fixture in fixtures:
            n = 1
            genericMethods.runPercentage(length,current,f"Running {current} fixture of {length}", "All data for all fixtures collected")
            home = fixture['team_h']
            away = fixture['team_a']
            teamNames = Teams.teamIDsAsKeysAndNamesAsData()
            homeName = teamNames[home]
            awayName = teamNames[away]
            homeScores = dict()
            homeGoals = list()
            homeWins = list()
            homeDraws = list()
            homeLosses = list()
            homeConceed = list()
            awayScores = dict()
            awayGoals = list()
            awayWins = list()
            awayDraws = list()
            awayLosses = list()
            awayConceed = list()

            while n < gw:
                for game in genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/fixtures/?event={n}'):
                    aScore = game['team_a_score']
                    hScore = game['team_h_score']
                    if game['team_h_score'] is None:
                        hScore = 0
                    if game['team_a_score'] is None:
                        aScore = 0
                        
                    if game['team_h'] == home:
                        homeGoals.append(hScore)
                        homeConceed.append(aScore)
                        if hScore < aScore:
                            homeLosses.append(1)
                        if hScore == aScore:
                            homeDraws.append(1)
                        if hScore > aScore:
                            homeWins.append(1)

                    if game['team_a'] == home:
                        homeGoals.append(aScore)
                        homeConceed.append(hScore)
                        if hScore > aScore:
                            homeLosses.append(1)
                        if hScore == aScore:
                            homeDraws.append(1)
                        if hScore < aScore:
                            homeWins.append(1)

                    if game['team_h'] == away:
                        awayGoals.append(hScore)
                        awayConceed.append(aScore)
                        if hScore < aScore:
                            awayLosses.append(1)
                        if hScore == aScore:
                            awayDraws.append(1)
                        if hScore > aScore:
                            awayWins.append(1)

                    if game['team_a'] == away:
                        awayGoals.append(aScore)
                        awayConceed.append(hScore)
                        if hScore > aScore:
                            awayLosses.append(1)
                        if hScore == aScore:
                            awayDraws.append(1)
                        if hScore < aScore:
                            awayWins.append(1)

                n += 1

            awayTeamScore = (sum(awayWins) * 3) + (sum(awayDraws))
            homeTeamScore = (sum(homeWins) * 3) + (sum(homeDraws))

            leaderboard[homeName] = homeTeamScore
            leaderboard[awayName] = awayTeamScore

            homeScores['goals'] = sum(homeGoals)
            homeScores['conceeded'] = sum(homeConceed)
            homeScores['wins'] = sum(homeWins)
            homeScores['draws'] = sum(homeDraws)
            homeScores['losses'] = sum(homeLosses)
            homeScores['score'] = homeTeamScore
            homeScores['id'] = home

            awayScores['goals'] = sum(awayGoals)
            awayScores['conceeded'] = sum(awayConceed)
            awayScores['wins'] = sum(awayWins)
            awayScores['draws'] = sum(awayDraws)
            awayScores['losses'] = sum(awayLosses)
            awayScores['score'] = awayTeamScore
            awayScores['id'] = away

            scores[homeName] = homeScores
            scores[awayName] = awayScores

            current += 1

        rankingsUnclean = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        rankings = genericMethods.reformattedSortedTupleAsDict(rankingsUnclean)

        winRankings = dict()

        while gw <= endGw:
            fixtures = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/fixtures/?event={gw}')
            length = len(fixtures)
            current = 1
            for fixture in fixtures:
                genericMethods.runPercentage(length,current,f"Running {current} fixture of {length}", "All data for all fixtures collected")
                home = fixture['team_h']
                homeName = teamNames[home]
                away = fixture['team_a']
                awayName = teamNames[away]
                try:
                    homeRankDifference = -(list(rankings.keys()).index(teamNames[home]) - list(rankings.keys()).index(teamNames[away]))
                    homeGoalsScoredDifference = scores[teamNames[home]]['goals'] + scores[teamNames[away]]['conceeded']
                    homeGoalsConceededDifference = scores[teamNames[home]]['conceeded'] + scores[teamNames[away]]['goals']
                    homeGoalsNet = homeGoalsScoredDifference - homeGoalsConceededDifference

                    awayGoalsScoredDifference = scores[teamNames[away]]['goals'] + scores[teamNames[home]]['conceeded']
                    awayGoalsConceededDifference = scores[teamNames[away]]['conceeded'] + scores[teamNames[home]]['goals']
                    awayGoalsNet = awayGoalsScoredDifference - awayGoalsConceededDifference

                    win = homeGoalsNet - awayGoalsNet

                    homePoints = win
                    awayPoints = -win

                    if homeName in winRankings:
                        existingRanking = winRankings[homeName]
                        winRankings[homeName] = existingRanking + homePoints
                    else:
                        winRankings[homeName] = homePoints

                    if awayName in winRankings:
                        existingRanking = winRankings[awayName]
                        winRankings[awayName] = existingRanking + awayPoints
                    else:
                        winRankings[awayName] = awayPoints
                except:
                    None

                current += 1
            gw += 1

        winUnclean = sorted(winRankings.items(), key=lambda x: x[1], reverse=True)
        easiestGames = genericMethods.reformattedSortedTupleAsDict(winUnclean)

        return easiestGames

# Returns all team names ask keys, with their associated team ID's
def teamNamesAsKeysAndIDsAsData():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
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
    for keys in readable['teams']:
        id = str.lower(keys['name'])
        name = keys['id']
        teams[name] = id
    return teams

# Returns all team ids ask keys, with their historic gameweek difficulty as a comma seperated list for each team
def teamIDsAsKeysAndGameweekDifficultyAsList(startGameweek, endGameweek):
    urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
    teamNames = Teams.teamIDsAsKeysAndNamesAsData()
    teams = dict()
    if startGameweek < 1:
        startGameweek = 1
    for teamID in teamNames:
        teamName = str.capitalize(teamNames[teamID])
        difficultyOfUpcomingGamesForTeam = list()
        currentGameweek = startGameweek
        while currentGameweek <= endGameweek:
            matched = False
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={currentGameweek}')
            for gameweekData in currentDumps:
                    if gameweekData['team_a'] == teamID:
                        difficultyOfUpcomingGamesForTeam.append(int(gameweekData['team_a_difficulty']))
                        matched = True
                    if gameweekData['team_h'] == teamID:
                        difficultyOfUpcomingGamesForTeam.append(int(gameweekData['team_h_difficulty']))
                        matched = True

            if matched == False:
                difficultyOfUpcomingGamesForTeam.append('-')

            currentGameweek += 1
        
        teams[teamID] = difficultyOfUpcomingGamesForTeam

    return teams

# Returns all team ids ask keys, with their associated players as a comma seperated list for each team
def teamIDsAsKeysAndPlayerIDsAsList():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for keys in readable['teams']:
        id = keys['id']
        playerIDs = list()
        for players in readable['elements']:
            if players['team'] == id:
                playerIDs.append(players['id'])
        teams[id] = playerIDs

    return teams

# Returns all team ids ask keys, with their associated players as a comma seperated list for each team
def playerIDsAsKeysAndTeamIDsAsList():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    readable = genericMethods.generateJSONDumpsReadable(url)
    teams = dict()
    for player in readable['elements']:
        teams[player['id']] = player['team']

    return teams

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
                difficultyOfUpcomingGamesForTeam.append('-')
                currentGameweek += 1

        return difficultyOfUpcomingGamesForTeam

# List the ID's of any team that has played in a given period

def allTeamsPlayingForAGameweek(gameweekNumber, maxGameweekNumber):
     urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
     teamsPlayed = list()
     while gameweekNumber <= maxGameweekNumber:
         currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweekNumber}')
         if not currentDumps:
             gameweekNumber += 1
         else:
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


# A method to pull the average goals conceded by gameweek difficulty for a particular team

def goalsconcededByDifficulty(idOfTheTeamWeWantToLookAt, gameweek, outliersIncluded):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        maxGameweek = gameweek
        gameweek = 1
        difficulty2 = list()
        difficulty3 = list()
        difficulty4 = list()
        difficulty5 = list()
        difficultyOfGamesWithGoalsconcededListed = dict()
        while gameweek < maxGameweek:
            teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(gameweek, gameweek)
            if teamID in teamsPlayingInCurrentPeriod:
                currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweek}')
                for gameweekData in currentDumps:
                        if gameweekData['team_a'] == teamID:
                            if gameweekData['team_h_score'] != None:
                                if gameweekData['team_h_score'] <= 5:
                                    gameweekDifficulty = gameweekData['team_a_difficulty']
                                    if gameweekDifficulty == 2:
                                        if outliersIncluded == False and gameweekData['team_h_score'] >= 4:
                                            None
                                        else:
                                            difficulty2.append(gameweekData['team_h_score'])
                                    if gameweekDifficulty == 3:
                                        if outliersIncluded == False and gameweekData['team_h_score'] >= 4:
                                            None
                                        else:
                                            difficulty3.append(gameweekData['team_h_score'])
                                    if gameweekDifficulty == 4:
                                        if outliersIncluded == False and gameweekData['team_h_score'] >= 4:
                                            None
                                        else:
                                            difficulty4.append(gameweekData['team_h_score'])
                                    if gameweekDifficulty == 5:
                                        if outliersIncluded == False and gameweekData['team_h_score'] >= 4:
                                            None
                                        else:
                                            difficulty5.append(gameweekData['team_h_score'])
                            gameweek += 1
                        if gameweekData['team_h'] == teamID:
                            if gameweekData['team_a_score'] != None:
                                if gameweekData['team_a_score'] <= 5:
                                    gameweekDifficulty = gameweekData['team_h_difficulty']
                                    if gameweekDifficulty == 2:
                                        if outliersIncluded == False and gameweekData['team_a_score'] >= 4:
                                            None
                                        else:
                                            difficulty2.append(gameweekData['team_a_score'])
                                    if gameweekDifficulty == 3:
                                        if outliersIncluded == False and gameweekData['team_a_score'] >= 4:
                                            None
                                        else:
                                            difficulty3.append(gameweekData['team_a_score'])
                                    if gameweekDifficulty == 4:
                                        if outliersIncluded == False and gameweekData['team_a_score'] >= 4:
                                            None
                                        else:
                                            difficulty4.append(gameweekData['team_a_score'])
                                    if gameweekDifficulty == 5:
                                        if outliersIncluded == False and gameweekData['team_a_score'] >= 4:
                                            None
                                        else:
                                            difficulty5.append(gameweekData['team_a_score'])
                            gameweek += 1
            else:
                gameweek += 1

        
        difficultyOfGamesWithGoalsconcededListed[2] = difficulty2
        difficultyOfGamesWithGoalsconcededListed[3] = difficulty3
        difficultyOfGamesWithGoalsconcededListed[4] = difficulty4
        difficultyOfGamesWithGoalsconcededListed[5] = difficulty5

        averageGoalsByDifficulty = dict()

        for difficulty in difficultyOfGamesWithGoalsconcededListed:
            if len(difficultyOfGamesWithGoalsconcededListed[difficulty]) != 0:
                averageGoalsconceded = round(genericMethods.listAverage(difficultyOfGamesWithGoalsconcededListed[difficulty]) , 1)  
                averageGoalsByDifficulty[difficulty] = averageGoalsconceded

        return averageGoalsByDifficulty

# A method to pull the average goals scored gameweek difficulty for a particular team

def goalsScoredByDifficulty(idOfTheTeamWeWantToLookAt, gameweek, outliersIncluded):
        teamID = idOfTheTeamWeWantToLookAt
        urlBase = 'https://fantasy.premierleague.com/api/fixtures/'
        maxGameweek = gameweek
        gameweek = 1
        difficulty2 = list()
        difficulty3 = list()
        difficulty4 = list()
        difficulty5 = list()
        difficultyOfGamesWithGoalsScoredListed = dict()
        while gameweek < maxGameweek:
            teamsPlayingInCurrentPeriod = Teams.allTeamsPlayingForAGameweek(gameweek, gameweek)
            genericMethods.runPercentage(maxGameweek,gameweek, "Gathering goals scored by difficulty", "Completed: Goals scored by difficulty")
            if teamID in teamsPlayingInCurrentPeriod:
                currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}/?event={gameweek}')
                for gameweekData in currentDumps:
                        if gameweekData['team_a'] == teamID:
                            if gameweekData['team_a_score'] != None:
                                gameweekDifficulty = gameweekData['team_a_difficulty']
                                if gameweekDifficulty == 2:
                                    if outliersIncluded == False and gameweekData['team_a_score'] >= 4:
                                        None
                                    else:
                                        difficulty2.append(gameweekData['team_a_score'])
                                if gameweekDifficulty == 3:
                                    if outliersIncluded == False and gameweekData['team_a_score'] >= 4:
                                        None
                                    else:
                                        difficulty3.append(gameweekData['team_a_score'])
                                if gameweekDifficulty == 4:
                                    if outliersIncluded == False and gameweekData['team_a_score'] >= 4:
                                        None
                                    else:
                                        difficulty4.append(gameweekData['team_a_score'])
                                if gameweekDifficulty == 5:
                                    if outliersIncluded == False and gameweekData['team_a_score'] >= 4:
                                        None
                                    else:
                                        difficulty5.append(gameweekData['team_a_score'])
                            gameweek += 1
                        if gameweekData['team_h'] == teamID:
                            if gameweekData['team_h_score'] != None:
                                gameweekDifficulty = gameweekData['team_h_difficulty']
                                if gameweekDifficulty == 2:
                                    if outliersIncluded == False and gameweekData['team_h_score'] >= 4:
                                        None
                                    else:
                                        difficulty2.append(gameweekData['team_h_score'])
                                if gameweekDifficulty == 3:
                                    if outliersIncluded == False and gameweekData['team_h_score'] >= 4:
                                        None
                                    else:
                                        difficulty3.append(gameweekData['team_h_score'])
                                if gameweekDifficulty == 4:
                                    if outliersIncluded == False and gameweekData['team_h_score'] >= 4:
                                        None
                                    else:
                                        difficulty4.append(gameweekData['team_h_score'])
                                if gameweekDifficulty == 5:
                                    if outliersIncluded == False and gameweekData['team_h_score'] >= 4:
                                        None
                                    else:
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

def generateLikelihoodToScoreByTeamForNextGame(gameweek, outliersIncludedBool):
    teamIDsAndNames = Teams.teamIDsAsKeysAndNamesAsData()
    teamDifficultyReference = dict()
    nextGameDifficultyByTeam = dict()
    length = len(teamIDsAndNames) - 1

    for teamID in teamIDsAndNames:
        teamName = teamIDsAndNames[teamID]
        teamDifficultyReference[teamID] = Teams.goalsScoredByDifficulty(teamID, gameweek, outliersIncludedBool)
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

def generateLikelihoodToConceedByTeamForNextGame(gameweek, outliersIncludedBool):
    teamIDsAndNames = Teams.teamIDsAsKeysAndNamesAsData()
    teamDifficultyReference = dict()
    nextGameDifficultyByTeam = dict()
    length = len(teamIDsAndNames) - 1

    for teamID in teamIDsAndNames:
        teamName = teamIDsAndNames[teamID]
        teamDifficultyReference[teamID] = Teams.goalsconcededByDifficulty(teamID, gameweek, outliersIncludedBool)
        nextGameDifficultyByTeam[teamID] = Teams.nextGameDifficulty(teamID, gameweek)

        currentIndex = list(teamIDsAndNames.keys()).index(teamID)
        genericMethods.runPercentage(length, currentIndex, "Gathering team difficulty and goals conceded index", "Complete: Gathered team difficulty and goals conceded index")

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
           homeStrengthOverall = keys['strength_overall_away']
           awayStrengthOverall = keys['strength_overall_home']
           awayStrengthDefence = keys['strength_defence_away']
           awayStrengthAttack = keys['strength_attack_away']
           homeStrengthDefence = keys['strength_defence_home']
           homeStrengthAttack = keys['strength_attack_home']
           strength['homeOverall'] = homeStrengthOverall
           strength['awayOverall'] = awayStrengthOverall
           strength['homeDefence'] = homeStrengthDefence
           strength['homeAttack'] = homeStrengthAttack
           strength['awayDefence'] = awayStrengthDefence
           strength['awayAttack'] = awayStrengthAttack
           teams[id] = strength

    return teams

def goalEconomyByTeamForGameweek(gameweek):

    gameweekSummaryJSON = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/fixtures/?event={gameweek}')
    shotsOnTargetByTeam = dict()
    goalEconomyByTeam = dict()
    teamIDs = Teams.teamIDsAsKeysAndNamesAsData()

    # Initialise the data

    penaltiesSaved = 0
    penaltiesMissed = 0
    goalsScored = 0
    saves = 0

    for fixture in gameweekSummaryJSON:
        stats = fixture['stats']
        for teamID in teamIDs:
            if teamID == fixture['team_a'] or teamID == fixture['team_h']:
                if teamID == fixture['team_a']:
                    teamStatus = 'home'
                else:
                    teamStatus = 'away'
                for element in stats:
                    if element['identifier'] =="goals_scored":
                        statsHome = element['h']
                        homeLen = len(statsHome)
                        statsAway = element['a']
                        awayLen = len(statsAway)
                        if awayLen > 0 and teamStatus == 'away':
                            goalsScoredList = list()
                            for result in statsAway:
                                goalsScoredList.append(result['value'])
                            goalsScored = sum(goalsScoredList)
                        if homeLen > 0 and teamStatus == 'home':
                            goalsScoredList = list()
                            for result in statsHome:
                                goalsScoredList.append(result['value'])
                            goalsScored = sum(goalsScoredList)
                    if element['identifier'] =="penalties_saved":
                        statsHome = element['h']
                        homeLen = len(statsHome)
                        statsAway = element['a']
                        awayLen = len(statsAway)
                        if awayLen > 0  and teamStatus == 'home':
                            penaltiesSavedList = list()
                            for result in statsAway:
                                penaltiesSavedList.append(result['value'])
                            penaltiesSaved = sum(penaltiesSavedList)
                        if homeLen > 0  and teamStatus == 'away':
                            penaltiesSavedList = list()
                            for result in statsHome:
                                penaltiesSavedList.append(result['value'])
                            penaltiesSaved = sum(penaltiesSavedList)
                    if element['identifier'] =="saves":
                        statsHome = element['h']
                        homeLen = len(statsHome)
                        statsAway = element['a']
                        awayLen = len(statsAway)
                        if awayLen > 0  and teamStatus == 'home':
                            savesList = list()
                            for result in statsAway:
                                savesList.append(result['value'])
                            saves = sum(savesList)
                        if homeLen > 0 and teamStatus == 'away' :
                            savesList = list()
                            for result in statsHome:
                                savesList.append(result['value'])
                            saves = sum(savesList)
                     
                shotsOnTarget = saves + penaltiesSaved + goalsScored
                shotsOnTargetByTeam[teamID] = shotsOnTarget	

                if shotsOnTarget != 0:
                    goalEconomy = round(((goalsScored / shotsOnTarget)*100), 2)
                else: 
                    goalEconomy = 0
                goalEconomyByTeam[teamID] = goalEconomy


    return goalEconomyByTeam

def goalEconomyByGameweekDifficultyByTeam():
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

    teamIDs = Teams.teamIDsAsKeysAndNamesAsData()
    gameweekDifficulty = Teams.teamIDsAsKeysAndGameweekDifficultyAsList(1, lastWeek)

    goalEconomyByGameweekDifficultyByTeam = dict()

    for team in teamIDs:
        difficulty2 = list()
        difficulty3 = list()
        difficulty4 = list()
        difficulty5 = list()
        goalEconomyByGameweekDifficulty = dict()
        currentWeek = 0
        lastWeek = genericMethods.generateCurrentGameweek() - 1
        teamList = gameweekDifficulty[team]
        genericMethods.runPercentage(20, team, f"Running team {team} of 20", "All of the teams have now been run successfully")
        gameweekDifficultyForTeam = gameweekDifficulty[team]
        while currentWeek <= lastWeek:
            weekDifficulty = gameweekDifficultyForTeam[currentWeek]
            weekGoalEconomy = goalEconomyByGameweek[currentWeek + 1]
            
            try:
                teamWeekGoalEconomy = weekGoalEconomy[team]
                if weekDifficulty == 2:
                        difficulty2.append(teamWeekGoalEconomy)
                if weekDifficulty == 3:
                        difficulty3.append(teamWeekGoalEconomy)
                if weekDifficulty == 4:
                        difficulty4.append(teamWeekGoalEconomy)
                if weekDifficulty == 5:
                        difficulty5.append(teamWeekGoalEconomy)

                currentWeek += 1

            except:
                currentWeek += 1
        
        if len(difficulty2) > 0:
                goalEconomyByGameweekDifficulty[2] = genericMethods.listAverage(difficulty2)
        else:
            goalEconomyByGameweekDifficulty[2] = 0
        if len(difficulty3) > 0:
            goalEconomyByGameweekDifficulty[3] = genericMethods.listAverage(difficulty3)
        else: 
            goalEconomyByGameweekDifficulty[3] = 0
        if len(difficulty4) > 0:
            goalEconomyByGameweekDifficulty[4] = genericMethods.listAverage(difficulty4)
        else:
            goalEconomyByGameweekDifficulty[4] = 0
        if len(difficulty5) > 0:
            goalEconomyByGameweekDifficulty[5] = genericMethods.listAverage(difficulty5)
        else:
            goalEconomyByGameweekDifficulty[5] = 0

        goalEconomyByGameweekDifficultyByTeam[team] = goalEconomyByGameweekDifficulty

    return goalEconomyByGameweekDifficultyByTeam


def goalEconomyByTeam():
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

    teamIDs = Teams.teamIDsAsKeysAndNamesAsData()
    gameweekDifficulty = Teams.teamIDsAsKeysAndGameweekDifficultyAsList(1, lastWeek)

    goalEconomyByTeam = dict()

    for team in teamIDs:
        economy = list()
        currentWeek = 0
        lastWeek = genericMethods.generateCurrentGameweek() - 1
        teamList = gameweekDifficulty[team]
        genericMethods.runPercentage(20, team, f"Running team {team} of 20", "All of the teams have now been run successfully")
        gameweekDifficultyForTeam = gameweekDifficulty[team]
        while currentWeek <= lastWeek:
            weekDifficulty = gameweekDifficultyForTeam[currentWeek]
            weekGoalEconomy = goalEconomyByGameweek[currentWeek + 1]
            
            try:
                teamWeekGoalEconomy = weekGoalEconomy[team]
                economy.append(teamWeekGoalEconomy)
                currentWeek += 1

            except:
                currentWeek += 1
        
        goalEconomyByTeam[team] = genericMethods.listAverage(economy)

    return goalEconomyByTeam

# Pull the data for a single users fantasy team
def getTeamDetails(teamID, username, password, gameweekNumber, isMyTeam):
    url = f'https://fantasy.premierleague.com/api/entry/{teamID}/event/{gameweekNumber}/picks/'
    Response = Teams.loginToSecureURL(url, username, password)  
    Data = Response.json()
    Dumps = json.dumps(Data)
    readableData = json.loads(Dumps)
    return readableData

def getCurrentTeamDetails(teamID, username, password):
    url = f'https://fantasy.premierleague.com/api/my-team/{teamID}'
    Response = Teams.loginToSecureURL(url, username, password)  
    Data = Response.json()
    Dumps = json.dumps(Data)
    readableData = json.loads(Dumps)
    return readableData

# Returns the influence of each player in order for a given gameweek
def teamInfluence(gameweekOfInterest):
        urlBase = 'https://fantasy.premierleague.com/api/'
        teamDict = dict()
        teams = teamIDsAsKeysAndNamesAsData()
        maxLen = len(teams)
        for team in teams:
            currentLen = list(teams.keys()).index(team) + 1
            genericMethods.runPercentage(maxLen, currentLen, f"Running team {currentLen} of {maxLen}", "Data collected for all of the teams")
            playersInTeam = generateListOfPlayerIDsAsKeysForTeam(team)
            playerDict = dict()
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}bootstrap-static/')     
            for player in playersInTeam:
                for gameweekData in currentDumps['elements']:
                    influence = float(gameweekData['influence'])
                    playerID = gameweekData['id']
                    if player == playerID:
                        playerDict[playerID] = influence

            teamDict[team] = playerDict

        return teamDict
    
# Returns the influence of each player with the player ID as a reference for a given timeframe
def teamInfluenceInAGivenTimeFrame(endGameweek, numberOfDaysToLookBack):
        urlBase = 'https://fantasy.premierleague.com/api/'
        teamDict = dict()
        teams = teamIDsAsKeysAndNamesAsData()
        maxLen = len(teams)
        for team in teams:
            teamData = list()
            currentLen = list(teams.keys()).index(team) + 1
            genericMethods.runPercentage(maxLen, currentLen, f"Running team {currentLen} of {maxLen}", "Data collected for all of the teams")
            playersInTeam = generateListOfPlayerIDsAsKeysForTeam(team)
            playerDict = dict() 
            for player in playersInTeam:
                currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}element-summary/{player}/')
                for record in currentDumps['history']:
                    round = record['round']
                    if record['round'] > (endGameweek - numberOfDaysToLookBack):
                        teamData.append(float(record['influence']))

            teamDict[team] = sum(teamData)

        return teamDict

# Returns the influence of each player in order for a given gameweek weighted by their average minutes on the pitch
def weightedTeamInfluence(gameweekOfInterest):
        urlBase = 'https://fantasy.premierleague.com/api/'
        teamDict = dict()
        teams = teamIDsAsKeysAndNamesAsData()
        maxLen = len(teams)
        for team in teams:
            currentLen = list(teams.keys()).index(team) + 1
            genericMethods.runPercentage(maxLen, currentLen, f"Running team {currentLen} of {maxLen}", "Data collected for all of the teams")
            playersInTeam = generateListOfPlayerIDsAsKeysForTeam(team)
            players = list()
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}bootstrap-static/')     
            for player in playersInTeam:
                avgMinutes = playerData.averageMinutesPlayed(player, gameweekOfInterest)
                percentageMinutes = avgMinutes / 90 if avgMinutes != 0 else 0
                for gameweekData in currentDumps['elements']:
                    if gameweekData['id'] == player:
                        influence = float(gameweekData['influence'])
                        influenceMinutes = influence * percentageMinutes
                        players.append(influenceMinutes)
                        break

            teamInfluence = sum(players)
            teamDict[team] = teamInfluence

        return teamDict

# TODO: Potentially merge these two methods 

# Returns the influence of each player in order for a given gameweek weighted by their average minutes on the pitch, and adjusted to account for injuries
def adjustedTeamInfluence(gameweekOfInterest):
        urlBase = 'https://fantasy.premierleague.com/api/'
        teamDict = dict()
        teams = teamIDsAsKeysAndNamesAsData()
        maxLen = len(teams)
        for team in teams:
            currentLen = list(teams.keys()).index(team) + 1
            genericMethods.runPercentage(maxLen, currentLen, f"Running team {currentLen} of {maxLen}", "Data collected for all of the teams")
            playersInTeam = generateListOfPlayerIDsAsKeysForTeam(team)
            players = list()
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}bootstrap-static/')     
            for player in playersInTeam:
                avgMinutes = playerData.averageMinutesPlayed(player, gameweekOfInterest)
                percentageMinutes = avgMinutes / 90 if avgMinutes != 0 else 0
                for gameweekData in currentDumps['elements']:
                    if gameweekData['id'] == player:
                        influence = float(gameweekData['influence'])
                        chanceOfPlaying = float(gameweekData['chance_of_playing_next_round']/100) if gameweekData['chance_of_playing_next_round'] is not None else 1
                        influenceMinutes = influence * percentageMinutes * chanceOfPlaying
                        players.append(influenceMinutes)
                        break

            teamInfluence = sum(players)
            teamDict[team] = teamInfluence

        return teamDict

# Returns the factor of each player in order for a given gameweek
def teamFactor(gameweekOfInterest):
        urlBase = 'https://fantasy.premierleague.com/api/'
        teamDict = dict()
        nextGameweek = gameweekOfInterest + 1
        teams = teamIDsAsKeysAndNamesAsData()
        teamGamweekDifficulty = teamIDsAsKeysAndGameweekDifficultyAsList(nextGameweek, nextGameweek)
        maxLen = len(teams)
        for team in teams:
            currentLen = list(teams.keys()).index(team) + 1
            genericMethods.runPercentage(maxLen, currentLen, f"Running team {currentLen} of {maxLen}", "Data collected for all of the teams")
            playersInTeam = generateListOfPlayerIDsAsKeysForTeam(team)
            playerDict = dict()
            currentDumps = genericMethods.generateJSONDumpsReadable(f'{urlBase}bootstrap-static/')     
            for player in playersInTeam:
                for gameweekData in currentDumps['elements']:
                    playerID = gameweekData['id']
                    if player == playerID:
                        teamId = gameweekData['team']
                        if isinstance(teamGamweekDifficulty[teamId][0], int) == True:
                            gameweekFactor = 6 - int(teamGamweekDifficulty[teamId][0])
                        else:
                            gameweekFactor = 0
                        ict = float(gameweekData['ict_index'])
                        totalPoints = int(gameweekData['total_points'])
                        minutes = int(gameweekData['minutes'])
                        pointsPerMinute = totalPoints / minutes if minutes else 0
                        factor = ict * pointsPerMinute * gameweekFactor
                        playerDict[playerID] = factor

            teamDict[team] = playerDict

        return teamDict


# Returns the total goals for team
def totalTeamGoals():
    teamDict = dict()
    teams = teamIDsAsKeysAndNamesAsData()
    maxLen = len(teams)
    currentGameweek = genericMethods.generateCurrentGameweek()
    for team in teams:
        currentLen = list(teams.keys()).index(team) + 1
        gw = 1
        genericMethods.runPercentage(maxLen, currentLen, f"Running team {currentLen} of {maxLen}", "Data collected for all of the teams")
        goalsList = list()
        while gw <= currentGameweek:
            gameweekData = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/fixtures/?event={gw}')
            if len(gameweekData) != 0:
                for fixture in gameweekData:
                    if team == fixture['team_a']:
                        goalsList.append(int(fixture['team_a_score']))
                        gw += 1
                        break
                    if team == fixture['team_h']:
                        goalsList.append(int(fixture['team_h_score']))
                        gw += 1
                        break
                if team != fixture['team_a'] and team != fixture['team_h']:
                    gw += 1
            else:
                goalsList.append(0)
                gw += 1


        goalsScored = sum(goalsList)
        teamDict[team] = goalsScored

    return teamDict

# Returns the total goals for team
def teamIDsAsKeysAndPercentageStrengthAsData(gameweek):
    urlBase = 'https://fantasy.premierleague.com/api/'
    teamDict = dict()
    teams = teamIDsAsKeysAndNamesAsData()
    maxLen = len(teams)
    totalAvailableInfluence = weightedTeamInfluence(gameweek)
    currentTeamInfluence = adjustedTeamInfluence(gameweek)
    for team in teams:
        currentLen = list(teams.keys()).index(team) + 1
        genericMethods.runPercentage(maxLen, currentLen, f"Running team {currentLen} of {maxLen}", "Data collected for all of the teams")
        percentageStrength = currentTeamInfluence[team] / totalAvailableInfluence[team]
        teamDict[team] = percentageStrength

    return teamDict

# Input if it's your team or not and get an up to date dict of your team make up

def getMyTeam(gw):
    myTeam = input("Is this your team (y/n) > ")
    myId = input("Team Id (mine is: 307954 / bot: 4279913 ) > ")
    currentGW = genericMethods.generateCurrentGameweek()

    if 'y' in myTeam:
        user = input("Username > ")
        password = input("Password > ")
        myTeam = getCurrentTeamDetails(myId, user, password)
    elif 'n' in myTeam:
        if gw >= currentGW:
            gw = gw - 1
        myTeam = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/entry/{myId}/event/{gw}/picks/')
    else:
        if gw > currentGW:
            gw = gw - 1
        myTeam = genericMethods.generateJSONDumpsReadable(f'https://fantasy.premierleague.com/api/entry/{myId}/event/{gw}/picks/')

    return myTeam