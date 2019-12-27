#####################################

team1 = ["Vojta2", "Vanan", "Vdolek"]
team2 = ["Roman", "Filip", "Marta"]

score1 = 10
score2 = 2

season = 3
session = 3

#####################################

import pandas as pd

file_name = "Orlovna.csv"

df = pd.read_csv(file_name)

df = df.append({
		'Season': season,
		'Session': session,
		'Player1_1': team1[0],
		'Player1_2': team1[1],
		'Player1_3': team1[2],
		'Player2_1': team2[0],
		'Player2_2': team2[1],
		'Player2_3': team2[2],
		'Score1': score1,
		'Score2': score2
	}, ignore_index = True)

df.to_csv(file_name, index=None)
