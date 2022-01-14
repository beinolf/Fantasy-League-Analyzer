from turtle import position
from data_helpers import DataHelper
from ast import literal_eval

from classes.player_week import PlayerWeek
from classes.team import Team
from classes.player_ref import PlayerRef

class DataProcessors:
    def __init__(self) -> None:
        self.dh = DataHelper()

    def get_draft_rosters(self, roster_size, league_size):
        player_arr = self.dh.get_player_arr()
        draft_tid_map = self.dh.get_draft_tid_map()
        teams = []
        for p in range(1, league_size + 1):
            intial_roster = []
            draft_pos = league_size + 1 - p
            team_id = draft_tid_map.get(str(draft_pos))
            team = Team(team_id)
            for i in range(1, roster_size + 1):
                if (i % 2 == 0):
                    pick = (i - 1) * league_size + p
                else:
                    pick = i * league_size - p + 1
                player = player_arr[pick - 1]
                intial_roster.append(PlayerRef(player[0], player[2], player[1]))
                i = i + 1
            team.add_drafted_roster(intial_roster)
            teams.append(team)
        return teams

    def get_weekly_roster(self, week, team_id):
        roster = []
        player_data_dict = self.dh.get_player_dict()
        player_week = self.dh.get_week_data(week, team_id)
        player_refs = literal_eval(player_week[1])
        for player_ref in player_refs:
            player_data = player_data_dict.get(player_ref[0])
            weekly_points_string = player_data[1]
            weekly_points_arr = literal_eval(weekly_points_string)
            weekly_points = weekly_points_arr[week]
            player_id = player_ref[0]
            player_poistion = player_data[0]
            benched = player_ref[1]
            player = PlayerWeek(weekly_points, player_id, player_poistion, benched)
            roster.append(player)
        return roster
        
    def get_weekly_opponent(self, week, team_id):
        week = self.dh.get_week_data(week, team_id)
        return week[2]
