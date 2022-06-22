from operator import pos
from turtle import position
from data_helpers import DataHelper

class PlayerWeek:
    def __init__(self, ps, pid, pos, b):
        self.points_scored = float(ps)
        self.player_id = int(pid)
        self.position = pos
        self.benched = b

    def set_benched(self, b):
        self.benched = b

    def print(self):
        print('pid: ' + str(self.player_id))
        print('points: ' + str(self.points_scored))
        print('pos: '+ str(self.position))
        print('')
