import Soccer as s

s.eval_match(['Vojta', 'Filip'], ['Vanan', 'Vdolek'], 10, 7)
s.eval_match(['Vojta', 'Vdolek'], ['Vanan', 'Filip'], 18, 16)
s.eval_match(['Vojta', 'Vdolek'], ['Vanan', 'Filip'], 10, 5)
s.eval_match(['Vojta', 'Honza'], ['Vanan', 'Filip'], 10, 7)
s.eval_match(['Vojta', 'Filip'], ['Vanan', 'Honza'], 10, 8)
s.eval_match(['Vojta', 'Vanan'], ['Filip', 'Honza'], 10, 5)
s.eval_match(['Vojta', 'Honza'], ['Filip', 'Vanan'], 10, 6)

s.export_games('Results/KopaniZaBarakem_Games.csv')
s.export_results('Results/KopaniZaBarakem_Results.txt')
s.export_ratings('Results/KopaniZaBarakem_Ratings.csv')