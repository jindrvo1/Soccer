import Soccer as s

s.eval_match(['Vojta1', 'Vojta2', 'Krystof'], ['Vdolek', 'Marta', 'Vanan'], 10, 8)
s.eval_match(['Marta', 'Vojta1', 'Krystof'], ['Vdolek', 'Vojta2', 'Vanan'], 2, 5)
s.eval_match(['Marek', 'Vojta2', 'Vdolek'], ['Vojta1', 'Vanan', 'Marta'], 11, 13)
s.eval_match(['Marta', 'Vojta2', 'Marek'], ['Vdolek', 'Vojta1', 'Vanan'], 6, 2)
	
s.print_ladders()
print()

elo_sug, ts_sug = s.suggest_match(['Vojta1', 'Vojta2', 'Vanan', 'Vdolek', 'Marta', 'Krystof'])

print("Elo suggestion: {} vs {}".format(elo_sug[0], elo_sug[1]))
print("Trueskill suggestion: {} vs {}".format(ts_sug[0], ts_sug[1]))