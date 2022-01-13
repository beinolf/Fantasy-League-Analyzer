import csv

players = {}
with open('data/player_data.csv', newline='') as pd:
            reader = csv.reader(pd)
            player_data = list(reader)
            
            for player in player_data:
                players.update({player[0]: [player[1], player[2]]})

print(players)