import csv
from ast import literal_eval
from pathlib import Path
from classes.player_ref import PlayerRef
from classes.team import Team

class DataHelper:
    def get_player_arr(self):
        if (Path('./data/player_data.csv').is_file()):
            with open('data/player_data.csv', newline='') as pd:
                reader = csv.reader(pd)
                return list(reader)
        else:
            return []

    def get_player_dict(self):
        players = {}
        player_data = self.get_player_arr()
    
        for player in player_data:
            players.update({ player[0]: [ player[1], player[2] ] })

        return players
    
    def get_draft(self):
        with open('data/draft.csv', newline='') as draft:
            reader = csv.reader(draft)
            draft_data = list(reader)
            
        return draft_data

    def get_draft_tid_map(self):
        with open('data/draft_tid_map.csv', newline='\n') as map_file:
            reader = csv.reader(map_file)
            draft_map = dict(reader)

        return draft_map

    def get_def_pid_map(self):
        with open('data/def_pid_map.csv', newline='\n') as map_file:
            reader = csv.reader(map_file)
            def_map = dict(reader)

        return def_map

    def get_player_roster(self, week, pid):
        with open('data/week_' + str(week) + ".csv", newline='') as draft:
            reader = csv.reader(draft)
            week = list(reader)

        return literal_eval(week[pid - 1][1])

    def get_week_data(self, week, pid):
        with open('data/week_' + str(week) + ".csv", newline='') as draft:
            reader = csv.reader(draft)
            week = list(reader)

        return week[pid - 1]