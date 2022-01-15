
from copy import deepcopy
import re


class Superlatives:

    def get_point_sort(self, value):
        return float(value.points_scored)

    def get_best_ball_teams(self, teams):
        best_ball_teams = deepcopy(teams)

        for team in best_ball_teams:
            for roster in team.weekly_rosters:
                QBs = []
                RBs = []
                WRs = []
                Ks = []
                DEFs = []
                TEs = []
                FLEXs = []

                position_groups = [QBs, RBs, WRs, Ks, DEFs, TEs]
                
                for player in roster:
                    if player.position == 'QB':
                        QBs.append(player)
                    elif player.position == 'RB':
                        RBs.append(player)
                        FLEXs.append(player)
                    elif player.position == 'WR':
                        WRs.append(player)
                        FLEXs.append(player)
                    elif player.position == 'K':
                        Ks.append(player)
                    elif player.position == 'DEF':
                        DEFs.append(player)
                    elif player.position == 'TE':
                        TEs.append(player)
                        FLEXs.append(player)

                for group in position_groups:
                    group.sort(key=self.get_point_sort, reverse=True)

                for index, QB in enumerate(QBs):
                    if index == 0:
                        QB.set_benched(False)
                    else:
                        QB.set_benched(True)

                for index, RB in enumerate(RBs):
                    if index <= 1:
                        RB.set_benched(False)
                    else:
                        RB.set_benched(True)

                for index, WR in enumerate(WRs):
                    if index <= 2:
                        WR.set_benched(False)
                    else:
                        WR.set_benched(True)

                for index, TE in enumerate(TEs):
                    if index <= 0:
                        TE.set_benched(False)
                    else:
                        TE.set_benched(True)

                for index, K in enumerate(Ks):
                    if index <= 0:
                        K.set_benched(False)
                    else:
                        K.set_benched(True)

                for index, DEF in enumerate(DEFs):
                    if index <= 0:
                        DEF.set_benched(False)
                    else:
                        DEF.set_benched(True)

                for index, TE in enumerate(TEs):
                    if index <= 0:
                        TE.set_benched(False)
                    else:
                        TE.set_benched(True)

                FLEXs.sort(key=self.get_point_sort,reverse=True)

                for flex in FLEXs:
                    if flex.benched:
                        flex.set_benched(False)
                        break

        return best_ball_teams

    def get_position_group_points(self, teams, position, num_rosterable):
        position_results = {}
        for team in teams:
            points_scored = 0
            for roster in team.weekly_rosters:
                position_group = []

                for player in roster:
                    if re.search(position, player.position) and player.benched == False:
                        position_group.append(player)

                position_group.sort(key=self.get_point_sort,reverse=True)
            
                for starter in range(0, num_rosterable):
                    points_scored = round(position_group[starter].points_scored + points_scored, 2)
            
            position_results.update({ team.team_id: points_scored })

        return position_results

    def get_drafted_teams(self, teams):
        drafted_teams = deepcopy(teams)

        for team in drafted_teams:
            drafted_ids = []
            for drafted_player in team.drafted_roster:
                drafted_ids.append(int(drafted_player.player_id))
            for roster in team.weekly_rosters:
                for player in roster:
                    if player.player_id not in drafted_ids:
                        player.set_benched(True)
                        
        return drafted_teams

    def get_wire_teams(self, teams):
        wire_teams = deepcopy(teams)
        
        for team in wire_teams:
            drafted_ids = []
            for drafted_player in team.drafted_roster:
                drafted_ids.append(int(drafted_player.player_id))
            for roster in team.weekly_rosters:
                for player in roster:
                    if player.player_id not in drafted_ids:
                        player.set_benched(False)
                        
        return wire_teams
                