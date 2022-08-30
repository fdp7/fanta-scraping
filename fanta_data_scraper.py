from itertools import cycle
from random import randint
from re import T
from time import sleep
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
from termcolor import colored

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
    season = season.replace('/','-').split()
    matchweek = matchweek.split()

    # export to csv
    filepath = str(season[1]) + "/" + str(matchweek[1]) + "/"
    os.makedirs(filepath, exist_ok=True) 
    filename = filepath + team + '.csv'
    team_report.to_csv(filename)

# Get seasons
def get_seasons():
    
    url = 'https://www.fantacalcio.it/pagelle'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    seasons_list = soup.find(class_='filters mt-4 mb-2')
    seasons_list = seasons_list.find(attrs={'name':'season'})
    seasons_list = seasons_list.find_all('option')

    seasons = np.array('Seasons')
    for season in seasons_list:
        seasons = np.append(seasons,season)
    seasons = np.sort(seasons)[::-1]
    return seasons

# Get matchweeks
def get_matchweeks():
    
    url = 'https://www.fantacalcio.it/pagelle'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    matchweeks_list = soup.find(class_='filters mt-4 mb-2')
    matchweeks_list = matchweeks_list.find(attrs={'name':'matchweek'})
    matchweeks_list = matchweeks_list.find_all('option')

    matchweeks = np.array('MatchWeek')
    for matchweek in matchweeks_list:
        matchweeks = np.append(matchweeks,matchweek)
    return matchweeks

# Get teams
def get_teams(season):
    season = season.replace('/','-').split()
    page = requests.get('https://www.fantacalcio.it/pagelle/' + str(season[1]) + '/atalanta/1')
    soup = BeautifulSoup(page.text, 'html.parser')
    
    teams_list = soup.find(class_='filters mt-4 mb-2')
    teams_list = teams_list.find(attrs={'name':'team-name'})
    teams_list = teams_list.find_all('option')

    teams = np.array('Teams')
    for team in teams_list:
        teams = np.append(teams,team)
    return teams

seasons = get_seasons()

# Data Scraping for seasons,matchweek,teams
for season in seasons[1:len(seasons)-1]:
    matchweeks = get_matchweeks()
    for matchweek in matchweeks[1:]:
        teams = get_teams(season)
        i = 0
        for team in teams[1:]:
            i = i + 1
            if(i % 5 == 0):
                sleep(3)
            # rename season and matchweek
            s = season.replace('/','-').split()
            m = matchweek.split()

            # shuffle headers 
            ua = UserAgent()
            ua.update()
            headers = {'User-Agent': ua.random}

            url = 'https://www.fantacalcio.it/pagelle/' + str(s[1]) +'/'+ team.lower() + '/' + str(m[1])
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            print(colored("connected to " + team +" at " + url, 'green'))

            # Extract team's players and grades
            data_scraping(team, matchweek, season)