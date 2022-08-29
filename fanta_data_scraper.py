import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
from termcolor import colored
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS

def data_scraping(team, matchweek, season):
    
    # get the report list
    report = soup.find(class_='report-list')
    report_info = report.find_all(class_='player-info')

    # create array
    players = np.array(['Names'])
    grades = np.array(['Grades'])

    # extract data
    for report in report_info:
        player = report.find(class_='player-name player-link').text.strip()
        players = np.append(players, player)
        grade = report.find(class_='badge grade').text.strip()
        grades = np.append(grades, grade)

    # create table
    team_report = pd.DataFrame({'Names':players,'Grades':grades})

    # rename season and matchweek
    #season = season.replace('/','-').split()
    matchweek = matchweek.split()

    # export to csv
    filepath = str(season) + "/" + str(matchweek[1]) + "/"
    os.makedirs(filepath, exist_ok=True) 
    filename = filepath + team + '.csv'
    team_report.to_csv(filename)


# Start from first page
page = requests.get('https://www.fantacalcio.it/pagelle/2021-22/atalanta/1')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Get seasons
seasons_list = soup.find(class_='filters mt-4 mb-2')
seasons_list = seasons_list.find(attrs={'name':'season'})
seasons_list = seasons_list.find_all('option')

seasons = np.array('Seasons')
for season in seasons_list:
    seasons = np.append(seasons,season)

# Get matchweeks
matchweeks_list = soup.find(class_='filters mt-4 mb-2')
matchweeks_list = matchweeks_list.find(attrs={'name':'matchweek'})
matchweeks_list = matchweeks_list.find_all('option')

matchweeks = np.array('MatchWeek')
for matchweek in matchweeks_list:
    matchweeks = np.append(matchweeks,matchweek)

# Get teams
teams_list = soup.find(class_='filters mt-4 mb-2')
teams_list = teams_list.find(attrs={'name':'team-name'})
teams_list = teams_list.find_all('option')

teams = np.array('Teams')
for team in teams_list:
    teams = np.append(teams,team)

## Data Scraping for seasons,matchweek,teams
#for season in seasons[1:len(seasons)-2]:  
#    for matchweek in matchweeks[1:]:
#        for team in teams[1:]:
#        #team = random.choice(teams)
#        #teams = np.delete(teams,np.where(teams == team))
#            
#            # rename season and matchweek
#            s = season.replace('/','-').split()
#            m = matchweek.split()
#
#            # shuffle headers 
#            ua = UserAgent()
#            ua.update()
#            headers = {'User-Agent': ua.random}
#
#            #shuffle proxies
#            proxies = {'http': 'http://190.64.18.177:80'} 
#
#            #random sleep and connect
#            requests.get('https://translate.google.it/?hl=it')
#
#            url = 'https://www.fantacalcio.it/pagelle/' + str(s[1]) +'/'+ team.lower() + '/' + str(m[1])
#            page = requests.get(url, headers=headers, proxies=proxies)
#            soup = BeautifulSoup(page.text, 'html.parser')
#            print(colored("connected to " + team +" at " + url, 'red'))
#
#            # Extract team's players and grades
#            data_scraping(team, matchweek, season)

# Data Scraping for teams, matchweeks
for team in teams[1:]:
    for matchweek in matchweeks[1:]:

        # rename season and matchweek
        s = '2019-20'
        m = matchweek.split()

        # shuffle headers 
        ua = UserAgent()
        ua.update()
        headers = {'User-Agent': ua.random}

        url = 'https://www.fantacalcio.it/pagelle/' + str(s) +'/'+ team.lower() + '/' + str(m[1])
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        print(colored("connected to " + team +" at " + url, 'red'))

        # Extract team's players and grades
        data_scraping(team, matchweek, s)