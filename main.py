import csv
from pathlib import Path

from data_helpers import DataHelper
from data_processor import DataProcessor
from service_calls import ServiceCalls


league_id = 412227
roster_size = 16
season_length = 16
number_of_teams = 8 
sc = ServiceCalls(league_id)
dh = DataHelper()
dp = DataProcessor()

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


# teams = dp.assign_inital_rosters(roster_size)

# for team in teams:
#     team.print()