from EloForTeams import EloForTeams
from collections import OrderedDict
import itertools
import trueskill as ts
from math import ceil

elo = EloForTeams()
p = {}

ELO_MODEL = "elo"
TRUESKILL_MODEL = "trueskill"
ELO_DEFAULT_RATING = 1200

class Player(object):
	def __init__(self, name, elo = ELO_DEFAULT_RATING, trueskill = ts.Rating()):
		self.name = name
		self.ratings = {ELO_MODEL: [elo], TRUESKILL_MODEL: [trueskill]}

	def last_rating(self, model):
		return self.ratings[model][-1]

	def add_rating(self, model, rating):
		self.ratings[model].append(rating)

def eval_match(team1, team2, score1, score2):
	# Update players in dictionary
	for player in team1:
		if player not in p:
			p[player] = Player(player)

	for player in team2:
		if player not in p:
			p[player] = Player(player)

	# Update elos
	s = 0.5
	if score1 > score2:
		s = 1
	elif score1 < score2:
		s = 0

	t1 = [p[x].last_rating(ELO_MODEL) for x in team1]
	t2 = [p[x].last_rating(ELO_MODEL) for x in team2]

	t1_new, t2_new = elo.rate_match(t1, t2, s, 1-s)

	for player in team1:
		p[player].add_rating(ELO_MODEL, t1_new.pop(0))

	for player in team2:
		p[player].add_rating(ELO_MODEL, t2_new.pop(0))

	# Update trueskills
	ranks = [0.5, 0.5]
	if score1 > score2:
		ranks = [0, 1]
	elif score1 < score2:
		ranks = [1, 0]
 
	t1 = [p[x].last_rating(TRUESKILL_MODEL) for x in team1]
	t2 = [p[x].last_rating(TRUESKILL_MODEL) for x in team2]

	t1_new, t2_new = ts.rate([t1, t2], ranks=ranks)

	t1_new = list(t1_new)
	t2_new = list(t2_new)

	for player in team1:
		p[player].add_rating(TRUESKILL_MODEL, t1_new.pop(0))

	for player in team2:
		p[player].add_rating(TRUESKILL_MODEL, t2_new.pop(0))

def suggest_match(players = p, team_size = 3):
	teams = itertools.combinations(players, team_size)

	for player in players:
		if player not in p:
			p[player] = Player(player)

	elo_pred = []
	ts_pred = []

	for team in teams:
		t1_n = list(team)
		t2_n_comb = [x for x in players if x not in team]

		for t2_n in itertools.combinations(t2_n_comb, team_size):
			t2_n = list(t2_n)
			t1_elo = [p[x].last_rating(ELO_MODEL) for x in team]
			t2_elo = [p[x].last_rating(ELO_MODEL) for x in players if x not in team]

			t1_ts = [p[x].last_rating(TRUESKILL_MODEL) for x in team]
			t2_ts = [p[x].last_rating(TRUESKILL_MODEL) for x in players if x not in team]

			t1_p, t2_p = elo.predict_winner(t1_elo, t2_elo)
			elo_pred.append((abs(t1_p - t2_p), t1_n, t2_n))

			ts_pred.append((ts.quality([t1_ts, t2_ts]), t1_n, t2_n))

	return (min(elo_pred), max(ts_pred))

def match_quality(team1, team2):
	t1_elo, t2_elo, t1_ts, t2_ts = [], [], [], []
	for player in team1:
		if player not in p:
			t1_elo.append(ELO_DEFAULT_RATING)
			t1_ts.append(Raint())
		else:
			t1_elo.append(p[player].last_rating(ELO_MODEL))
			t1_ts.append(p[player].last_rating(TRUESKILL_MODEL))

	for player in team2:
		if player not in p:
			t2_elo.append(ELO_DEFAULT_RATING)
			t2_ts.append(Rating())
		else:
			t2_elo.append(p[player].last_rating(ELO_MODEL))
			t2_ts.append(p[player].last_rating(TRUESKILL_MODEL))

	elo_pred = elo.predict_winner(t1_elo, t2_elo)
	elo_quality = 1-abs(elo_pred[0]-elo_pred[1])
	ts_quality = ts.quality([t1_ts, t2_ts])

	return (elo_quality, ts_quality)

def get_player(player):
	if player in p:
		return (p[player].ratings[ELO_MODEL], p[player].ratings[TRUESKILL_MODEL])

def print_ladders():
	# Elo ladder
	elo_ladder_tmp = {k: v.last_rating(ELO_MODEL) for (k, v) in p.items()}
	elo_ladder = OrderedDict(reversed(sorted(elo_ladder_tmp.items(), key=lambda x:x[1])))

	print("------------------------")
	print("------ ELO ladder ------")
	print("------------------------")
	for name, rating in elo_ladder.items():
			print('{}: {}'.format(name, rating))

	# Trueskill ladder
	ts_ladder_tmp = {k: {'cse': v.last_rating(TRUESKILL_MODEL).mu - 3*v.last_rating(TRUESKILL_MODEL).sigma, 
							'mu': v.last_rating(TRUESKILL_MODEL).mu, 
							'sigma': v.last_rating(TRUESKILL_MODEL).sigma} 
					for (k, v) in p.items()}
	ts_ladder = OrderedDict(reversed(sorted(ts_ladder_tmp.items(), key=lambda x:x[1]['cse'])))

	print("------------------------")
	print("--- Trueskill ladder ---")
	print("------------------------")
	for name, rating in ts_ladder.items():
			print("{}: {} (mu = {}, sigma = {})".format(name, rating['cse'], rating['mu'], rating['sigma']))
