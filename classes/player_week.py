from operator import pos
from turtle import position
from data_helpers import DataHelper

class PlayerWeek:
    def __init__(self, ps, pid, pos, b):
        self.points_scored = ps
        self.player_id = pid
        self.position = pos
        self.benched = b

    def print(self):
        print('pid: ' + str(self.player_id))
        print('points: ' + str(self.points_scored))
        print('pos: '+ str(self.position))
        print('')
