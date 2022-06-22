
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

    def get_position_group_points(self, teams, position, num_rosterable, num_of_teams, season_length):
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
            
            position_results.update({ team.team_id: [points_scored, round(points_scored/season_length, 2)] })

        total_result = 0
        for t, r in position_results.items():
            total_result = round(total_result + r[0], 2)

        avg = round(total_result/num_of_teams, 2)

        position_results.update({num_of_teams + 1: [avg, round(avg/season_length, 2)]})

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
                    if player.player_id in drafted_ids and not player.benched:
                        player.set_benched(True)
                        
        return wire_teams
                
    def get_value_teams(self, teams, player_values, draft):
        drafted_teams = deepcopy(teams)
        player_value_maps = {}

        for team in drafted_teams:
            player_value_map = {}

            for drafted_player in team.drafted_roster:
                player_value_map.update({ int(drafted_player.player_id): 0})

            for roster in team.weekly_rosters:
                for player in roster:
                    if player.player_id in player_value_map and not player.benched:
                        curr_value = player_value_map.get(player.player_id)
                        player_value_map.update({ player.player_id: round(curr_value + player.points_scored, 2)})

            player_value_maps.update({ team.team_id: player_value_map })

        for tid, pvm in player_value_maps.items():
            for p in pvm:
                draft_pos = draft.index([str(p)])
                draft_value = float(player_values[draft_pos][0])
                season_value = pvm.get(p)
                pvm.update({p: round(season_value/draft_value, 2)})
                        
        return player_value_maps

    def get_bdgo(self, a_results, bb_results, num_of_weeks, num_of_teams):
        game_day_org = {}
        for tid, result in a_results.items():
            suboptimal = round(bb_results.get(tid).total_scores - result.total_scores, 2)
            game_day_org.update({tid: [suboptimal, round(suboptimal/num_of_weeks, 2)]})

        total_result = 0
        for t, r in game_day_org.items():
            total_result = round(total_result + r[0], 2)

        avg = total_result/num_of_teams

        game_day_org.update({num_of_teams + 1: [avg, round(avg/num_of_weeks, 2)]})
        return game_day_org

    def get_luck(self, a_results, bb_results, num_of_weeks, num_of_teams):
        luck_result = {}
        for tid, result in a_results.items():
            suboptimal = round(bb_results.get(tid).point_against - result.point_against, 2)
            luck_result.update({tid: [suboptimal, round(suboptimal/num_of_weeks, 2)]})

        total_result = 0
        for t, r in luck_result.items():
            total_result = round(total_result + r[0], 2)

        avg = round(total_result/num_of_teams, 2)

        luck_result.update({num_of_teams + 1: [avg, round(avg/num_of_weeks, 2)]})
        return luck_result

    def get_draft_sup(self, draft_val, num_of_weeks, num_of_teams):
        val_result = {}
        for tid, valmap in draft_val.items():
            total_val = 0
            for pid, val in valmap.items():
                total_val = round(total_val + val, 2)
            val_result.update({ tid: [total_val, round(total_val/num_of_weeks, 2)] })

        total_result = 0
        for t, r in val_result.items():
            total_result = round(total_result + r[0], 2)

        avg = round(total_result/num_of_teams, 2)

        val_result.update({num_of_teams + 1: [avg, round(avg/num_of_weeks, 2)]})
        return val_result
