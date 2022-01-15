from re import M
from turtle import position
from classes.season_result import SeasonResult
from data_helpers import DataHelper
from ast import literal_eval

from classes.player_week import PlayerWeek
from classes.team import Team
from classes.player_ref import PlayerRef
from classes.match_info import MatchInfo

class DataProcessors:
    def __init__(self) -> None:
        self.dh = DataHelper()

    def get_roster_teamid(self, value):
        return value.team_id

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
        teams.sort(key=self.get_roster_teamid)
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
            weekly_points = weekly_points_arr[week - 1]
            player_id = player_ref[0]
            player_poistion = player_data[0]
            benched = player_ref[1]
            player = PlayerWeek(weekly_points, player_id, player_poistion, benched)
            roster.append(player)
        return roster
        
    def get_weekly_opponent(self, week, team_id):
        week = self.dh.get_week_data(week, team_id)
        return week[2]

    def get_match(self, teams, team_id, week):
        team_roster = teams[team_id - 1].weekly_rosters[week - 1]
        opponent_id = teams[team_id - 1].opponents[week - 1]
        opponent_roster = teams[opponent_id - 1].weekly_rosters[week - 1]
        rosters = { team_id: team_roster, opponent_id: opponent_roster }
        scores = {}
        intial_pid = 0
        for pid, players in rosters.items():
            score = 0

            for player in players:
                if not player.benched:
                    score = score + float(player.points_scored)
            scores.update({ pid: round(score,2) })

            if len(scores) == 2:
                if scores.get(pid) > scores.get(intial_pid):
                    winner_id = pid
                    loser_id = intial_pid
                else:
                    winner_id = intial_pid
                    loser_id = pid
            else:
                intial_pid = pid

        return MatchInfo(rosters, winner_id, loser_id, scores) 

    def get_season_matches(self, teams, season_length):
        all_matches = []
        for week in range(1, season_length + 1):
            week_matches = {}
            for team in teams:
                match = self.get_match(teams, team.team_id, week)
                if (str(match.winner_id) + str(match.loser_id) not in week_matches.keys()):
                    week_matches.update({ str(match.winner_id) + str(match.loser_id): match })
            all_matches.append(week_matches)
        return all_matches

    def process_matches(self, matches, number_of_teams):
        season_results = {}
        for pid in range(1, number_of_teams + 1):
            season_results.update({ pid: SeasonResult(0, 0, 0, 0) })
        
        for week in matches:
            for match in week.values():
                loser = season_results.get(match.loser_id)
                loser.add_loss()
                loser.add_to_total(match.scores.get(match.loser_id))
                loser.add_to_against(match.scores.get(match.winner_id))
                winner = season_results.get(match.winner_id)
                winner.add_win()
                winner.add_to_total(match.scores.get(match.winner_id))
                winner.add_to_against(match.scores.get(match.loser_id))

        return season_results
                