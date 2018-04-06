import Soccer as s

s.eval_match(['Vojta1', 'Vojta2', 'Krystof'], ['Vdolek', 'Marta', 'Vanan'], 10, 8)
s.eval_match(['Marta', 'Vojta1', 'Krystof'], ['Vdolek', 'Vojta2', 'Vanan'], 2, 5)

s.eval_match(['Marek', 'Vojta2', 'Vdolek'], ['Vojta1', 'Vanan', 'Marta'], 11, 13)
s.eval_match(['Marta', 'Vojta2', 'Marek'], ['Vdolek', 'Vojta1', 'Vanan'], 6, 2)

s.eval_match(['Krystof', 'Panek', 'Vojta2'], ['Vanan', 'Klizka', 'Marek'], 10, 2)
s.eval_match(['Panek', 'Klizka', 'Vojta2'], ['Vanan', 'Krystof', 'Marek'], 10, 4)
s.eval_match(['Krystof', 'Vanan', 'Vojta2'], ['Klizka', 'Panek', 'Marek'], 10, 5)

s.eval_match(['Krystof', '-_-', 'Marta'], ['Vojta2', 'Vojta1', 'Vdolek'], 11, 9)
s.eval_match(['Krystof', '-_-', 'Vdolek'], ['Vojta2', 'Vojta1', 'Marta'], 9, 11)

s.eval_match(['Vojta2', 'Roman', 'Filip'], ['Vanan', 'Panek', 'Marta'], 10, 6)
s.eval_match(['Vojta2', 'Marta', 'Filip'], ['Vanan', 'Panek', 'Roman'], 3, 9)

s.eval_match(['Vojta2', 'Roman', 'Marta'], ['Vanan', 'Filip', 'Krystof'], 10, 7)
s.eval_match(['Vojta2', 'Roman', 'Filip'], ['Vanan', 'Marta', 'Krystof'], 2, 10)

s.eval_match(['Filip', 'Roman', 'Marta'], ['Vanan', 'Vojta2', 'Krystof'], 6, 10)
s.eval_match(['Vojta2', 'Roman', 'Marta'], ['Vanan', 'Filip', 'Krystof'], 3, 3)

s.eval_match(['Michal', 'Vanan', 'Vojta2'], ['Filip', 'Vojta1', 'Marta'], 10, 4)
s.eval_match(['Vojta2', 'Vojta1', 'Marta'], ['Michal', 'Filip', 'Vanan'], 3, 8)

s.eval_match(['Michal', 'Vanan', 'Vojta2'], ['Krystof', 'Vojta1', 'Marta'], 10, 7)
s.eval_match(['Vojta2', 'Vojta1', 'Marta'], ['Michal', 'Krystof', 'Vanan'], 10, 9)

s.eval_match(['Vojta1', 'Krystof', 'Vojta2'], ['Vanan', 'Filip', 'Roman'], 10, 8)
s.eval_match(['Vanan', 'Roman', 'Vojta2'], ['Vojta1', 'Krystof', 'Filip'], 11, 9)

s.eval_match(['Vojta2', 'Krystof', 'Vdolek'], ['Marek', 'Filip', 'Marta'], 10, 2)
s.eval_match(['Marta', 'Filip', 'Vojta2'], ['Vdolek', 'Krystof', 'Marek'], 10, 5)
s.eval_match(['Marek', 'Filip', 'Vojta2'], ['Krystof', 'Vdolek', 'Marta'], 10, 8)

s.eval_match(['Krystof', 'Vojta1', 'Vojta2'], ['Vanan', 'Filip', 'Skleny'], 2, 10)
s.eval_match(['Skleny', 'Vojta1', 'Vojta2'], ['Vanan', 'Filip', 'Krystof'], 7, 10)

s.export_games('Results/Orlovna_Games.csv')
s.export_results('Results/Orlovna_Results.txt')
s.export_ratings('Results/Orlovna_Ratings.csv')

#s.print_streaks()

#s.print_predictions()