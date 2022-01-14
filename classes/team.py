class Team:
    def __init__(self, tid):
        self.drafted_roster = []
        self.weekly_rosters = []
        self.team_id = int(tid)
        self.opponents = []

    def add_weekly_roster(self, ros):
        self.weekly_rosters.append(ros)

    def add_drafted_roster(self, dros):
        self.drafted_roster = dros

    def add_opponent(self, oppo):
        self.opponents.append(oppo)

    def print(self):
        print('drafted roster team ' + str(self.team_id))
        for player in self.drafted_roster:
            player.print()

        print('week rosters team ' + str(self.team_id))
        i = 1
        for roster in self.weekly_rosters:
            print('Week ' + str(i))
            for player in roster:
                player.print()
            i = i + 1
            print('-----------------------')
        print('*************************************************************')