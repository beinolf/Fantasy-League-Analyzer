from re import S


class SeasonResult:
    def __init__(self, w, l, ts):
        self.wins = w
        self.losses = l
        self.total_scores = ts

    def add_win(self):
        self.wins = self.wins + 1

    def add_loss(self):
        self.losses = self.losses + 1

    def add_to_total(self, game_score):
        self.total_scores = round(self.total_scores + game_score, 2)