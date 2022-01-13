from classes.position import Position
from data_helpers import DataHelper

class PlayerWeek:
    def __init__(self, ps, pid, pos, w):
        self.points_scored = ps
        self.player_id = pid
        self.week = w
        self.position = Position(pos)

    def ref_to_week(player_ref, w):
        dh = DataHelper()
        players = dh.get_player_dict()
        player_dict_val = players.get(player_ref.player_id)
        return PlayerWeek(player_dict_val[1][ w - 1 ], player_ref.player_id, player_dict_val[0], w)

    def print(self):
        print('pid:' + str(self.player_id))
        print('points:' + str((self.points_scored)))
        print('week:' + str(self.week))    