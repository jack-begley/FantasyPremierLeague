from bs4 import BeautifulSoup
import requests
import playerData
import genericMethods
import Teams
import gameweekSummary
import json
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import lxml
import random

def getPlayerStats(players):
    allStats = dict()
    seasonId = getCurrentSeasonId()
    for player in players:
        playerNumbers = dict()
        playerId = players[player]
        urlSafePlayer = str(player).replace(" ",'-')
        url = f"https://www.premierleague.com/players/{playerId}/{urlSafePlayer}/stats?co=1&se={seasonId}"
        playerRequest = requests.get(url)
        soup = BeautifulSoup(playerRequest.content, 'html.parser')
        playerStats = soup.find_all(class_="normalStat")
        for data in playerStats:
            if data != 'source':
                stats = float(str(data.contents[1].contents[1].contents[0]).replace(" ","").replace("\n", "").replace("%", "").replace(",", ""))
                label = str(data.contents[1].next.extract()).replace('"b',"").replace('"','').rstrip()
                playerNumbers[label] = stats
        allStats[player] = playerNumbers
    return allStats

def getPlayerStatsDetailed(players):
    allStats = dict()
    seasonId = getCurrentSeasonId()
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(r'C:\Users\JackBegley\Documents\GitHub\FantasyPremierLeague\chromeDrivers\chromedriver', desired_capabilities=capabilities)
    jsonList = list()
    for player in players:
        playerNumbers = dict()
        playerId = players[player]
        urlSafePlayer = str(player).replace(" ",'-')
        url = f"https://www.premierleague.com/players/{playerId}/{urlSafePlayer}/stats?co=1&se={seasonId}"
        time.sleep(random.randint(0, 100)/100)
        driver.get(f"url")
        pageContent = driver.page_source
        # XHR - minimise the logs, and parse in the "message" data as JSON.
        pageLogs = driver.get_log("performance")
        for log in pageLogs:
            message = json.loads(log['message'])
            try:
                if str(message['message']['params']['request']['url']).find('footballapi.pulselive.com') == True:
                    jsonList.append(message) 
            except:
                None
        
    driver.quit()
    
    return allStats

def getAllPlayers():
    currentSeasonID = getCurrentSeasonId()
    teamIDs = getTeamIDsWithNamesAsKeys()
    players = dict()
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(r'C:\Users\JackBegley\Documents\GitHub\FantasyPremierLeague\chromeDrivers\chromedriver', desired_capabilities=capabilities)
    for team in teamIDs:
        time.sleep(random.randint(0, 100)/100)
        driver.get(f"https://www.premierleague.com/players/?se={currentSeasonID}&cl={teamIDs[team]}")
        pageContent = driver.page_source
        soup = BeautifulSoup(pageContent, 'lxml')
        playerURLs = soup.find_all(class_="playerName")
        for player in playerURLs:
            playerName = player.contents[1]
            playerURL = player.contents[0].previous_element.attrs['href']
            playerIDResult = re.search('/players/(.+?)/', playerURL)
            playerID = int(playerIDResult.group(1))
            players[playerName] = playerID

    driver.quit()

    return players

def getTeamIDsWithNamesAsKeys():
    teamsSite = requests.get("https://www.premierleague.com/clubs")
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
    url = requests.get("https://www.premierleague.com/stats")
    currentSoup = BeautifulSoup(url.content, 'html.parser').find(class_="statsCard__button")
    seasonId = int(re.search('se=(.*)', currentSoup.attrs['href']).group(1))
    return seasonId

    

    

