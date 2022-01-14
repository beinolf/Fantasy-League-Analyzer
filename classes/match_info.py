class MatchInfo:
    def __init__(self, r):
        self.rosters = r
        self.scores = self.calculate_scores(r)

    def calculate_scores(self, rosters):
        scores = {}
        intial_pid = 0
        for pid, players in rosters.items():
            score = 0
            for player in players:
                if not player.benched:
                    score = score + float(player.points_scored)
            scores.update({ pid: round(score,2) })
            
            if len(scores) == 2:
                if scores.get(pid) > scores.get(intial_pid):
                    self.winner_id = pid
                    self.loser_id = intial_pid
                else:
                    self.winner_id = intial_pid
                    self.loser_id = pid
            else:
                intial_pid = pid

        return scores