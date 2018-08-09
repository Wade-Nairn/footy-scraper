# Variables for JSON object are written with an underscore eg game_data
# working variables are written in camelCase

from bs4 import BeautifulSoup
import requests
import json
import csv
import re

# Change this to a for loop that loods through player list?
# Create new player list with only players from 2010
player_url = 'https://afltables.com/afl/stats/players/S/Shaun_Atley.html'

def game_scraper(gameLink):
    gameSource = requests.get(gameLink).text
    gameData = BeautifulSoup(gameSource, "html.parser")
    # print(gameData)
    gameData = gameData.find("table").text
    gameData = gameData.split()
    print(gameData)
    date = gameData[6]
    time = gameData[7]
    ampm = gameData[8]
    print(date)
    print(time)
    print(ampm)
    audience = gameData[9:14]
    audience = ', '.join([str(x) for x in audience])
    audience = re.findall(r"[0-9\(\)]+", audience)
    # audience = str(audience[0])
    print(audience)
    ground = gameData[3]
    print(ground)
    # round_data["ground"] =
    # round_data["date"] =
    # round_data["audience"] =


def player_scraper(player_url):
    source = requests.get(player_url).text
    playerData = BeautifulSoup(source, "html.parser")

    player_data = {}
    seasonData = {}
    seasonList =[]

    player = playerData.find('h1').text
    tables = playerData.find_all('table')



    # Process the data for each season
    #ignore the first eight tables as the are not needed
    for table in tables[7:]:
        head = table.find('thead').text
        # which year is the current itteration on
        year = head[-64:-60]
        #which club was the player at for this year
        club = head[:-67]

        season_data = {}
        #add data to the jason object
        season_data["season"] = year
        season_data["club"] = club

        body = table.find_all('tr')
        roundData = []

        # Process the Round Data
        for data in body[:-1]:

            row = data.find_all('td')
            round_data = {}
            # i to create an index
            i = 0
            gameLinks = data.find_all('a')
            # print(gameLinks)

            for game in gameLinks:
                gameLink = str(game)
                # print(gameLink)
                newGameLink = gameLink[14:43]
                urlstr = "https://afltables.com/afl/stats"
                newGameLink = urlstr + newGameLink
                # print(newGameLink)

                #calls the game scraper function
                game_scraper(newGameLink)

            # Process the Rounds Stat
            for column in row[1:]:

                cell = column.text
                i += 1
                # if the cell is empty change the data to zero
                if cell == '\xa0':
                    cell = '0'

                # match the cells to the data
                # there must be a shorter way to do this
                if i == 2:
                    round_data["round"] = cell
                elif i == 1:
                    round_data["opponent"] = cell
                elif i == 3:
                    round_data["result"] = cell
                elif i == 4:
                    round_data["shirtNumber"] = cell
                elif i == 5:
                    round_data["kicks"] = cell
                elif i == 6:
                    round_data["marks"] = cell
                elif i == 7:
                    round_data["handballs"] = cell
                elif i == 8:
                    round_data["disposals"] = cell
                elif i == 9:
                    round_data["goals"] = cell
                elif i == 10:
                    round_data["behinds"] = cell
                elif i == 11:
                    round_data["hitouts"] = cell
                elif i == 12:
                    round_data["tackles"] = cell
                elif i == 13:
                    round_data["rebound50s"] = cell
                elif i == 14:
                    round_data["inside50s"] = cell
                elif i == 15:
                    round_data["clearances"] = cell
                elif i == 16:
                    round_data["clangers"] = cell
                elif i == 17:
                    round_data["freeKicksFor"] = cell
                elif i == 18:
                    round_data["freeKicksAgainst"] = cell
                elif i == 19:
                    round_data["brownlowVotes"] = cell
                elif i == 20:
                    round_data["contestedPossessions"] = cell
                elif i == 21:
                    round_data["uncontestedPossessions"] = cell
                elif i == 22:
                    round_data["contestedMarks"] = cell
                elif i == 23:
                    round_data["marksInside50"] = cell
                elif i == 24:
                    round_data["onePerecnters"] = cell
                elif i == 25:
                    round_data["bounces"] = cell
                elif i == 26:
                    round_data["goalAssists"] = cell
                elif i == 27:
                    round_data["percentOfGamePlayed"] = cell

                # print(i," ", cell)
            #print(round_data)
            roundData.append(round_data)
            # print(roundData)

        season_data["roundData"] = roundData
        # print(season_data)
        seasonList.append(season_data)

    player_data["seasonList"] = seasonList
    player_data["name"] = player

player_scraper(player_url)
