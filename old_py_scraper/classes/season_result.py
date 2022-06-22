from re import S

class SeasonResult:
    def __init__(self, w, l, ts, pa):
        self.wins = w
        self.losses = l
        self.total_scores = ts
        self.point_against = pa

    def add_win(self):
        self.wins = self.wins + 1

    def add_loss(self):
        self.losses = self.losses + 1

    def add_to_total(self, score):
        self.total_scores = round(self.total_scores + score, 2)

    def add_to_against(self, score_opp):
        self.point_against = round(self.point_against + score_opp, 2)