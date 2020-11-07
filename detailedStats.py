from bs4 import BeautifulSoup
import requests
import playerData
import genericMethods
import Teams
import gameweekSummary
import json
import re
from selenium import webdriver
import time

#driver = webdriver.Chrome(r'C:\Users\JackBegley\Documents\GitHub\FantasyPremierLeague\chromeDrivers\chromedriver')
#teams = "https://www.premierleague.com/clubs"
#teamsSite = driver.get(teams)

def getAllPlayers():
    currentSeasonID = getCurrentSeasonId()
    teamIDs = getTeamIDsWithNamesAsKeys()
    players = dict()
    for team in teamIDs:
        teamID = teamIDs[team]
        url = f"https://www.premierleague.com/players/?se={currentSeasonID}&cl={teamID}"
        playerSite = driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(playerSite.content, 'html.parser')
        playerURLs = soup.find_all(class_="playerName")
        for player in playerURLs:
            playerName = player.contents[1]
            playerURL = player.contents[0].previous_element.attrs['href']
            playerIDResult = re.search('/players/(.+?)/', playerURL)
            playerID = int(playerIDResult.group(1))
            players[playerName] = playerID

    return players

def getTeamIDsWithNamesAsKeys():
    soup = BeautifulSoup(teamsSite.content, 'html.parser')
    teamsURLs = soup.find_all(class_="indexItem")
    teamDict = dict()
    for teamURL in teamsURLs:
        teamResult = re.search('/clubs/(.+?)/', teamURL.attrs['href'])
        teamID = int(teamResult.group(1))
        teamNameResult = re.search(f'/{teamID}/(.+?)/overview', teamURL.attrs['href'])
        teamName = teamNameResult.group(1).replace("-"," ")
        teamDict[teamName] = teamID

    return teamDict

def getCurrentSeasonId():
    url = driver.get("https://www.premierleague.com/stats")
    time.sleep(2)
    currentSoup = (BeautifulSoup(url).content, 'html.parser').find(class_="statsCard__button")
    return int(re.search('se=(.*)', currentSoup.attrs['href']).group(1))

    

    


