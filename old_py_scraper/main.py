import csv
import imp
from pathlib import Path

from data_helpers import DataHelper
from data_processors import DataProcessors
from service_calls import ServiceCalls
from superlatives import Superlatives


league_id = 412227
roster_size = 16
season_length = 15
number_of_teams = 8 
sc = ServiceCalls(league_id)
dh = DataHelper()
dp = DataProcessors()
sup = Superlatives()

if (not Path('./data/draft_value.csv').is_file()):
    sc.set_draft_value()

if (not Path('./data/def_pid_map.csv').is_file()):
    sc.make_def_player_id_map()
else:
    print("Defense team id map already created")

if (not Path('./data/draft.csv').is_file()):
    sc.set_draft_data()
else:
    print("Draft data already created")

if (not Path('./data/draft_tid_map.csv').is_file()):
    sc.set_draftp_to_team_id()
else:
    print("Draft player id map already created")

if (not Path('./data/player_data.csv').is_file()):
    draft_data = dh.get_draft()
    for player_id in draft_data:
        sc.set_player_data(player_id[0])
else:
    print("Player data already created")

for week in range(1, season_length + 1):
    if (not Path('./data/week_' + str(week) + '.csv').is_file()):
        sc.set_weekly_data(week)
        for team in range (1, number_of_teams + 1):
            roster = dh.get_player_roster(week, team)
        for player in roster:
            sc.set_player_data(player[0])
    else:
       print("Week " + str(week) + " data already created")

teams = dp.get_draft_rosters(roster_size, number_of_teams)

for week in range(1, season_length + 1):
    for team in teams:
        roster = dp.get_weekly_roster(week, team.team_id)
        opponent = dp.get_weekly_opponent(week, team.team_id)
        team.add_weekly_roster(roster)
        team.add_opponent(opponent)

all_matches = dp.get_season_matches(teams, season_length)
results = dp.process_matches(all_matches, number_of_teams)

best_ball_teams = sup.get_best_ball_teams(teams)
best_ball_matches = dp.get_season_matches(best_ball_teams, season_length)
best_ball_results = dp.process_matches(best_ball_matches, number_of_teams) 

position_map = {'K':1, 'QB':1, 'RB':2, 'WR':3, 'TE':1, 'DEF':1}

position_results = {}
for position, min in position_map.items():
    position_results.update({ str(position): sup.get_position_group_points(teams, position, min, number_of_teams, season_length) })

drafted_teams = sup.get_best_ball_teams(teams)
drafted_matches = dp.get_season_matches(drafted_teams, season_length)
drafted_results = dp.process_matches(drafted_matches, number_of_teams)

wire_teams = sup.get_best_ball_teams(teams)
wire_matches = dp.get_season_matches(wire_teams, season_length)
wire_results = dp.process_matches(wire_matches, number_of_teams)

dv = dh.get_draft_value()
draft_data = dh.get_draft()

value = sup.get_value_teams(teams, dv, draft_data)

bdgo = sup.get_bdgo(results, best_ball_results, season_length, number_of_teams)
luck = sup.get_luck(results, best_ball_results, season_length, number_of_teams)
draft_val = sup.get_draft_sup(value, season_length, number_of_teams)
print('')
