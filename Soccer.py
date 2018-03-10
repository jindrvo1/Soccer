from EloForTeams import EloForTeams
from collections import OrderedDict
import itertools
import trueskill as ts
import csv
import sys
from math import ceil, log
from scipy.optimize import minimize

elo = EloForTeams()
p = {}
m = 0
matches = []

ELO_MODEL = "elo"
TRUESKILL_MODEL = "trueskill"
ELO_DEFAULT_RATING = 1200

class Player(object):
	def __init__(self, name, elo = ELO_DEFAULT_RATING, trueskill = ts.Rating()):
		self.name = name
		self.ratings = {ELO_MODEL: {0: elo}, TRUESKILL_MODEL: {0: trueskill}}
		self.games = {'won': 0, 'lost': 0, 'total': 0, 'goals': 0}

	def last_rating(self, model):
		return self.ratings[model][max(self.ratings[model])]

	def add_rating(self, model, rating, match):
		self.ratings[model][match] = rating

	def add_game(self, score, goals):
		if score == 1:
			self.games['won'] += 1
		elif score == 0:
			self.games['lost'] +=1

		self.games['goals'] += goals

		self.games['total'] += 1

def eval_match(team1, team2, score1, score2):
	# Update players in dictionary
	for player in team1:
		if player not in p:
			p[player] = Player(player)

	for player in team2:
		if player not in p:
			p[player] = Player(player)

	global m
	m += 1

	# Update elos
	s = 0.5
	if score1 > score2:
		s = 1
	elif score1 < score2:
		s = 0

	global matches
	matches.append((team1, team2, s))

	# game counter
	for player in team1:
		p[player].add_game(s, score1)
	for player in team2:
		p[player].add_game(1-s, score2)

	t1 = [p[x].last_rating(ELO_MODEL) for x in team1]
	t2 = [p[x].last_rating(ELO_MODEL) for x in team2]

	t1_new, t2_new = elo.rate_match(t1, t2, s, 1-s)

	for player in team1:
		p[player].add_rating(ELO_MODEL, t1_new.pop(0), m)

	for player in team2:
		p[player].add_rating(ELO_MODEL, t2_new.pop(0), m)

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
		p[player].add_rating(TRUESKILL_MODEL, t1_new.pop(0), m)

	for player in team2:
		p[player].add_rating(TRUESKILL_MODEL, t2_new.pop(0), m)

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

# function to minimize in the maximum-likelihood estimation
def log_likelihood(scores, matches):
	ll = 0

	for match in matches:
		numerator = sum([scores[x] if match[0][x] == 1 else 0 for x in range(len(scores))])
		denumerator = sum([scores[x] if (match[0][x] == 1 or match[1][x] == 1) else 0 for x in range(len(scores))])
		ll += match[2]*log(numerator/denumerator) + (1-match[2])*log(1-numerator/denumerator)

	ll /= -len(matches)

	return ll

def mle():
	m = []

	for match in matches:
		t1 = [1 if player in match[0] else 0 for player in p.keys()]
		t2 = [1 if player in match[1] else 0 for player in p.keys()]
		m.append((t1, t2, match[2]))

	init = [0.5 for player in p.keys()]
	bounds = [(0.001, 0.999) for player in p.keys()]

	res = minimize(log_likelihood, init, args=(m,), bounds=bounds)

	res_list = list(res.x)
	ratings = {}
	for id, player in p.items():
		ratings[id] = res_list.pop(0)
	
	return ratings

def get_player(player):
	if player in p:
		return (p[player].ratings[ELO_MODEL], p[player].ratings[TRUESKILL_MODEL])

def print_streaks():
	lws_p, lws_l = longest_winning_streak()
	lls_p, lls_l = longest_losing_streak()

	if (len(lws_p) > 1):
		print("Longest winning streak are currently holding {} with {} won games in a row!".format(''.join(x+' and ' if i != len(lws_p)-1 else x for i, x in enumerate(lws_l)), lws_l))
	else:
		print("Longest winning streak is currently holding {} with {} won games in a row!".format(''.join(lws_p), lws_l))

	if len(lls_p) > 1:
		print("Longest losing streak are currently holding {} with {} lost games in a row! Suckers!".format(''.join(x+' and ' if i != len(lls_p)-1 else x for i, x in enumerate(lls_p)), lls_l))
	else:
		print("Longest losing streak is currently holding {} with {} lost games in a row! Sucker!".format(''.join(lls_p), lls_l))

def longest_losing_streak():
	len_max = 0
	p_max = []
	for name, player in p.items():
		len = 0
		ratings = list(player.ratings[ELO_MODEL].values())[::-1]
		for i, r in enumerate(ratings):
			if ratings[i] < ratings[i+1]:
				len += 1
			else:
				break
		if len >= len_max:
			if len > len_max:
				p_max = []
			len_max = len
			p_max.append(name)

	return (p_max, len_max)

def longest_winning_streak():
	len_max = 0
	p_max = []
	for name, player in p.items():
		len = 0
		ratings = list(player.ratings[ELO_MODEL].values())[::-1]
		for i, r in enumerate(ratings):
			if ratings[i] > ratings[i+1]:
				len += 1
			else:
				break
		if len >= len_max:
			if len > len_max:
				p_max = []
			len_max = len
			p_max.append(name)

	return (p_max, len_max)


def print_ladders():
	# Elo ladder
	elo_ladder_tmp = {k: v.last_rating(ELO_MODEL) for (k, v) in p.items()}
	elo_ladder = OrderedDict(reversed(sorted(elo_ladder_tmp.items(), key=lambda x:x[1])))

	print("-----------------------------------")
	print("----------- ELO ladder ------------")
	print("-----------------------------------")
	for name, rating in elo_ladder.items():
			print('{}: {}'.format(name, rating))

	# Trueskill ladder
	ts_ladder_tmp = {k: {'cse': v.last_rating(TRUESKILL_MODEL).mu - 3*v.last_rating(TRUESKILL_MODEL).sigma, 
							'mu': v.last_rating(TRUESKILL_MODEL).mu, 
							'sigma': v.last_rating(TRUESKILL_MODEL).sigma} 
					for (k, v) in p.items()}
	ts_ladder = OrderedDict(reversed(sorted(ts_ladder_tmp.items(), key=lambda x:x[1]['cse'])))

	print("-------------------------------------")
	print("--------- Trueskill ladder ----------")
	print("-------------------------------------")
	for name, rating in ts_ladder.items():
			print("{}: {} (mu = {}, sigma = {})".format(name, rating['cse'], rating['mu'], rating['sigma']))

	# MLE ladder
	mle_ladder_tmp = mle()
	mle_ladder = OrderedDict(reversed(sorted(mle_ladder_tmp.items(), key=lambda x:x[1])))

	print("-------------------------------------")
	print("--- Maximum-likelihood estimation ---")
	print("-------------------------------------")
	for name, rating in mle_ladder.items():
		print("{}: {}".format(name, rating))

def get_games(player = None):
	games = {}

	if player is None:
		for player in p:
			games[player] = p[player].games
	else:
		games = p[player].games

	return games

def export_games(file):
	with open(file, 'w') as file:
		fieldnames = ['player', 'total', 'won', 'lost', 'goals']
		writer = csv.DictWriter(file, fieldnames=fieldnames)

		writer.writeheader()

		for name, player in p.items():
			writer.writerow({'player': name, 'total': player.games['total'], 'won': player.games['won'], 'lost': player.games['lost'], 'goals': player.games['goals']})

def export_results(file):
	sys.stdout = open(file, 'w')
	print_ladders()
	print()
	sys.stdout = sys.__stdout__

def export_ratings(file):
	with open(file, 'w') as file:
		global m
		
		fieldnames = ['player']

		for i in range(0, m+1):
			fieldnames.append('elo_{}'.format(i))

		for i in range(0, m+1):
			fieldnames.append('ts_{}'.format(i))

		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()

		for name, player in p.items():
			row = {}
			row['player'] = name

			for i in range(0, m+1):
				if i in player.ratings[ELO_MODEL]:
					row['elo_{}'.format(i)] = player.ratings[ELO_MODEL][i]
				else:
					j = i
					while j > 0:
						j -= 1
						if j in player.ratings[ELO_MODEL]:
							row['elo_{}'.format(i)] = player.ratings[ELO_MODEL][j]
							break

			for i in range(0, m+1):
				if i in player.ratings[TRUESKILL_MODEL]:
					row['ts_{}'.format(i)] = player.ratings[TRUESKILL_MODEL][i].mu - 3*player.ratings[TRUESKILL_MODEL][i].sigma
				else:
					j = i
					while j > 0:
						j -= 1
						if j in player.ratings[TRUESKILL_MODEL]:
							row['ts_{}'.format(i)] = player.ratings[TRUESKILL_MODEL][j].mu - 3*player.ratings[TRUESKILL_MODEL][j].sigma
							break

			writer.writerow(row)
