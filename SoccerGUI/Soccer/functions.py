import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import norm

from . import SoccerAPI as s
from .models import Match

def _eval_match(match):
    s.eval_match(
        [pl.name for pl in match.team1.all()],
        [pl.name for pl in match.team2.all()],
        match.score1,
        match.score2
    )

def _eval_matches():
    matches = Match.objects.all().order_by('pk')

    for match in matches:
        _eval_match(match)

def _reset():
    s.reset()

def get_all_ratings():
    _eval_matches()
    ret = s.get_all_ratings()
    _reset()
    return ret

def get_player(player):
    _eval_matches()
    ret = s.get_player(player)
    _reset()
    return ret

def get_all_games():
    _eval_matches()
    ret = s.get_games()
    _reset()
    return ret

def get_games(player):
    _eval_matches()
    ret = s.get_games(player)
    _reset()
    return ret

def get_winning_streak(player):
    _eval_matches()
    ret = s.winning_streak(player)
    _reset()
    return ret

def get_losing_streak(player):
    _eval_matches()
    ret = s.losing_streak(player)
    _reset()
    return ret

def get_streaks(player):
    _eval_matches()
    ret = (s.winning_streak(player), s.losing_streak(player))
    _reset()
    return ret

def get_longest_winning_streak(player):
    _eval_matches()
    ret = s.longest_winning_streak_player(player)
    _reset()
    return ret

def get_longest_losing_streak(player):
    _eval_matches()
    ret = s.longest_losing_streak_player(player)
    _reset()
    return ret

def get_longest_streaks(player):
    _eval_matches()
    ret = (s.longest_winning_streak_player(player), s.longest_losing_streak_player(player))
    _reset()
    return ret

def get_longest_winning_streaks():
    _eval_matches()
    ret = s.longest_winning_streak_players()
    _reset()
    return ret

def get_longest_losing_streaks():
    _eval_matches()
    ret = s.longest_losing_streak_players()
    _reset()
    return ret

def _eval_matches_at(match):
    matches = Match.objects.filter(pk__lte=match.pk)
    past_matches = []
    for match in matches:
        for past_match in past_matches:
            _eval_match(past_match)
        _eval_match(match)

def _get_all_ratings_at(match):
    _eval_matches_at(match)
    ret = s.get_all_ratings()
    _reset()
    return ret

def get_all_ratings_at():
    matches = Match.objects.all()
    ret = {}
    for match in matches:
        ret[match.pk] = _get_all_ratings_at(match)

    return ret

def elo_predict(t1, t2):
    return s.predict(t1, t2)


################################
# ============================ #
################################

def get_rating_development_plot(ratings):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x = [i for i in range(len(ratings[0].values()))],
            y = list(ratings[0].values()),
            name = 'Elo'
        ),
        secondary_y = False
    )
    fig.add_trace(
        go.Scatter(
            x = [i for i in range(len(ratings[1]['cse']))],
            y = ratings[1]['cse'],
            name = 'TrueSkill'
        ),
        secondary_y = True
    )
    fig.add_trace(
        go.Scatter(
            x = [i for i in range(len(ratings[0].values()))],
            y = [1200 for i in range(len(ratings[0].values()))],
            name = 'Elo mean',
            opacity = 0.4
        ),
        secondary_y=False
    )
    fig.update_layout(title_text="Vývoj Elo/TS")
    fig.update_xaxes(title_text="Zápasi")
    fig.update_yaxes(title_text="Elo", secondary_y=False)
    fig.update_yaxes(title_text="TrueSkill", secondary_y=True)

    return plot(fig, auto_open=False, output_type="div")

def get_trueskill_development_plot(trueskills):
    fig = go.Figure()
    n = len(trueskills['mu'])
    opacity = 0.1
    opacity_inc = 0.9/n

    for i in range(n):
        mu = trueskills['mu'][i]
        sigma = trueskills['sigma'][i]
        color = 'red' if i+1 == n else 'blue'
        x = np.linspace(norm.ppf(0.01, mu, sigma), norm.ppf(0.99, mu, sigma), 100)
        fig.add_trace(go.Scatter(
            x = x,
            y = norm.pdf(x, mu, sigma),
            line = {'color': color},
            opacity = opacity,
            name = f"Hra {i}"
        ))
        opacity += opacity_inc

    fig.update_layout(title_text="Vývoj TS")
    fig.update_xaxes(title_text="Skill")
    fig.update_yaxes(title_text="Probability density")

    return plot(fig, auto_open=False, output_type="div")