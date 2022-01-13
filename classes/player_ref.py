class PlayerRef:
    def __init__(self, pid, pts, pos):
        if pts != None:
            self.points = pts
        else:
            self.points = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        if pos != None:
            self.position = pos
        else:
            self.position = ''

        self.player_id = pid

    def add_week(self, week, p):
        self.points[week - 1] = p
    
    def add_pos(self, pos):
        self.position = pos
    
    def print(self):
        print(self.points)
        print(' ')  
        print(self.player_id)
        print(' ') 
        print(self.position) 
        print('\n')  
