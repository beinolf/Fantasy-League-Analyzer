class Team:
    def __init__(self, tid):
        self.drafted_roster = []
        self.weekly_rosters = []
        self.team_id = tid

    def add_weekly_roster(self, ros):
        self.weekly_rosters.append(ros)

    def add_drafted_roster(self, dros):
        self.drafted_roster.append(dros)

    def print(self):
        print('drafted roster team ' + str(self.team_id))
        for roster in self.drafted_roster:
            for player in roster:
                player.print()
        print('-------------')