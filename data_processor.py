from data_helpers import DataHelper
from classes.team import Team
from classes.player_ref import PlayerRef

class DataProcessor:
        def __init__(self) -> None:
            self.dh = DataHelper()

        def assign_inital_rosters(self, num_of_rounds) -> Team:
            player_arr = self.dh.get_player_arr()
            draft_tid_map = self.dh.get_draft_tid_map()
            num_of_teams = len(draft_tid_map)
            teams = []

            for p in range(1, num_of_teams + 1):
                intial_roster = []
                team = Team(draft_tid_map.get(9 - p))

                for i in range(1, num_of_rounds + 1):
                    if (i % 2 == 0):
                        pick = (i - 1) * num_of_teams + p
                    else:
                        pick = i * num_of_teams - p + 1
                    player = player_arr[pick - 1]
                    intial_roster.append(PlayerRef(player[0], player[2], player[1]))
                    i = i + 1

                team.add_drafted_roster(intial_roster)
                teams.append(team)
            return teams