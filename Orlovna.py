#%%
import Soccer as s
import pandas as pd

#%%
df = pd.read_csv('Orlovna.csv')

for id, row in df.iterrows():
    s.eval_match(
        [
            row.Player1_1,
            row.Player1_2,
            row.Player1_3
        ],
        [
            row.Player2_1,
            row.Player2_2,
            row.Player2_3
        ], 
        row.Score1, 
        row.Score2
    )

#%%
s.export_games('Results/Orlovna_Games.csv')
s.export_results('Results/Orlovna_Results.txt')
s.export_ratings('Results/Orlovna_Ratings.csv')
