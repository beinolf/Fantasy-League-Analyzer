from asyncio import sleep
import csv
from operator import truediv
import re
from os import link, read
import requests
import time
from bs4 import BeautifulSoup

from classes.player_ref import PlayerRef
from data_helpers import DataHelper

class ServiceCalls:
    def __init__(self, lid) -> None:
        self.dh = DataHelper()
        self.league_id = lid
        self.base_url = 'https://football.fantasysports.yahoo.com/f1/' + str(lid)

    def set_draft_value(self):
        value_url = 'https://www.theringer.com/nfl/2018/8/20/17758898/fantasy-football-draft-pick-value-chart'
        value_html = requests.get(value_url).text
        value_soup = BeautifulSoup(value_html, 'html.parser')
        values = []

        table = value_soup.find('table', { 'class': "p-data-table" })
        for tr in table.find_all('tr'):
            values.append(tr.contents[3].next)

        values.pop(0)
        values.pop(0)

        with open('data/draft_value.csv', 'w', newline='') as draft:   
            wtr = csv.writer(draft,lineterminator='\n')
            for value in values:
                wtr.writerow([value])

    # Will create drafts.csv, a csv file containing a csv of player_ids in drafted order
    def set_draft_data(self):
        ff_url = self.base_url + '/draftresults'
        html_text = requests.get(ff_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        def_pid_map = self.dh.get_def_pid_map()
        player_ids = []
        
        for link in soup.find_all('a'):
            if link.get('href').startswith('https://sports.yahoo.com/nfl/players'):
                player_id = link.get('href').replace('https://sports.yahoo.com/nfl/players/', "")
                player_ids.append(player_id)
            elif link.get('href').startswith('https://sports.yahoo.com/nfl/teams'):
                tname = link.get('href').replace('https://sports.yahoo.com/nfl/teams/', "").replace("/", "")
                player_id = def_pid_map.get(tname)
                player_ids.append(player_id)

        with open('data/draft.csv', 'w', newline='') as draft:   
            wtr = csv.writer(draft,lineterminator='\n')
            for player in player_ids:
                wtr.writerow([player])

    def set_weekly_data(self, week):
        time.sleep(.1)
        ff_url = self.base_url + '/starters?week=' + str(week)
        html_text = requests.get(ff_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        def_pid_map = self.dh.get_def_pid_map()

        for table in soup.find_all('table', { 'id': re.compile(r'^Tst-team-\b([1-9]|1[0-4])\b$') }):
            roster = []
            team_id = table['id'].replace("Tst-team-", "")
            tbody = table.find('tbody')

            for tr in tbody.find_all('tr'):
                benched = tr.contents[1].contents[0] == 'BN' or tr.contents[1].contents[0] == 'IR'
                link = tr.find('a')

                if link.get('href').startswith('https://sports.yahoo.com/nfl/players'):
                    player_id = link.get('href').replace('https://sports.yahoo.com/nfl/players/', "").replace("/news", "")

                elif link.get('href').startswith('https://sports.yahoo.com/nfl/teams'):
                    tname = link.get('href').replace('https://sports.yahoo.com/nfl/teams/', "").replace("/", "")
                    player_id = def_pid_map.get(tname)
                
                roster.append([player_id, benched])

            matchup_url = self.base_url + '/matchup?week=' + str(week) + '&mid1=' + str(team_id)
            matchup_text = requests.get(matchup_url).text
            matchup_soup = BeautifulSoup(matchup_text, 'html.parser')

            matchup_link = matchup_soup.find('a', { 'href': re.compile(self.base_url + r'/(?!' + str(team_id) + r')')})
            matchup_id = matchup_link.get('href').replace(self.base_url, "").replace("/", "") 
        
            with open('data/week_' + str(week) + '.csv', 'a', newline='') as weekcsv:
                wtr = csv.writer(weekcsv)
                wtr.writerow([team_id, roster, matchup_id])

    def set_draftp_to_team_id(self):
        draft_url = self.base_url + '/draftresults'
        draft_text = requests.get(draft_url).text
        draft_soup = BeautifulSoup(draft_text, 'html.parser')

        ff_url = self.base_url + '/starters?week=1'
        html_text = requests.get(ff_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        tname_tid_map = {}
        draftp_tid_map = {}

        for link in soup.find_all('a', { 'href':re.compile( r'^/f1/' + str(self.league_id) + r'/\b([1-9]|1[0-4])\b$') }): 
            tname = link.contents[0]
            tid = link.get('href').replace('/f1/' + str(self.league_id) + '/', "")
            tname_tid_map.update( { tname: tid } )
        
        draft_arr = draft_soup.find('div', {'id':'drafttables'}).find('tbody').contents

        for i in range(1, len(tname_tid_map) + 1):
            dtname = draft_arr[i * 2 - 1].contents[5].attrs['title']
            tid_val = tname_tid_map.get(dtname)
            draftp_tid_map.update( { i: tid_val } )

        with open('data/draft_tid_map.csv', 'w') as draft_map:
             wtr = csv.writer(draft_map)
             for key, value in draftp_tid_map.items():
                wtr.writerow([key, value])

    def set_player_data(self, player_id):
        player_dict = self.dh.get_player_dict()

        if player_dict.get(player_id) == None:
            with open('data/player_data.csv', 'a') as player_data_file:
                time.sleep(.1)
                ff_url = self.base_url + '/playernote?init=1&view=notes&pid=' + str(player_id)
                html_text = requests.get(ff_url, timeout=100).text
                soup = BeautifulSoup(html_text, 'html.parser')
                scrapped_player = PlayerRef(player_id, None, None)
                week = 1

                for td in soup.find_all('td'):
                    if td['class'][0] == '\\"fanpts\\"':
                        scrapped_player.add_week(week, td.next.rstrip("<\/td>"))
                        week = week + 1
                    elif td['class'][0] == '\\"opp\\"' and td.next.replace('<\/td>', "") == 'BYE':
                        scrapped_player.add_week(week, 0)
                        week = week + 1

                for dd in soup.find_all('dd'):
                    if dd.has_attr('class') and dd['class'][0] == '\\"pos\\"':
                        scrapped_player.add_pos(dd.next.rstrip('<span>|<\/span><\/dd>'))

                wtr = csv.writer(player_data_file, delimiter=',',lineterminator='\n')
                wtr.writerow([scrapped_player.player_id, scrapped_player.position, scrapped_player.points])

            print('added player ')
            scrapped_player.print()
            print('------------')
        else:
            print('Player ' + str(player_id) + ' already in data')

    def make_def_player_id_map(self):
        d_url = self.base_url + '/players?&sort=AR&sdir=1&status=ALL&pos=DEF&stat1=S_S_2021&jsenabled=1'
        d_text = requests.get(d_url).text
        d_soup = BeautifulSoup(d_text, 'html.parser')
        dmap = {}

        for link in d_soup.find_all('a', { 'href': re.compile(r'^https://sports.yahoo.com/nfl/teams/'), 'class': re.compile(r'^playernote') }):
            pid = link.get('data-ys-playerid')
            name = link.get('href').replace('https://sports.yahoo.com/nfl/teams/', "").replace("/", "")
            dmap.update({ name: pid })

        d_url = self.base_url + '/players?status=ALL&pos=DEF&cut_type=9&stat1=S_S_2021&myteam=0&sort=AR&sdir=1&count=25'
        d_text = requests.get(d_url).text
        d_soup = BeautifulSoup(d_text, 'html.parser')

        for link in d_soup.find_all('a', { 'href': re.compile(r'^https://sports.yahoo.com/nfl/teams/'), 'class': re.compile(r'^playernote') }):
            pid = link.get('data-ys-playerid')
            name = link.get('href').replace('https://sports.yahoo.com/nfl/teams/', "").replace("/", "")
            dmap.update({ name: pid })
        
        with open('data/def_pid_map.csv', 'w', newline='') as draft_map:
            wtr = csv.writer(draft_map)
            for key, value in dmap.items():
                wtr.writerow([key, value])
        