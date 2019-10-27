from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage

import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots

from . import functions as f
from .models import Player, Match, Rating
from .forms import MatchNewForm

def matches(request):
    matches = Match.objects.all().order_by('-pk')
    ratings, predictions, correctly_predicited = {}, {}, {}

    for match in matches:
        team1 = [pl.name for pl in match.team1.all()]
        team2 = [pl.name for pl in match.team2.all()]
        rs = [r for r in match.rating.all()]
        team1_elo, team1_ts, team1_mse = [], [], []
        team2_elo, team2_ts, team2_mse = [], [], []

        for rating in rs:
            pl_rs = Player.objects.get(name=rating.player.name).ratings.all()
            rating_before = Rating()
            rating_before.player = rating.player
            for i, r in enumerate(pl_rs):
                if r == rating and i != 0:
                    rating_before = pl_rs[i-1]
                    
            if rating.player.name in team1:
                team1_elo.append(rating_before.elo)
                team1_ts.append({'mu': rating_before.mu, 'sigma': rating_before.sigma})
                team1_mse.append(rating_before.mse)
            if rating.player.name in team2:
                team2_elo.append(rating_before.elo)
                team2_ts.append({'mu': rating_before.mu, 'sigma': rating_before.sigma})
                team2_mse.append(rating_before.mse)

        ratings[match.id] = (
            {
                'elo': team1_elo,
                'ts': team2_ts, 
                'mse': team2_mse
            }, 
            {
                'elo': team2_elo,
                'ts': team2_ts,
                'mse': team2_mse
            }
        )

        predictions[match.id] = f.elo_predict(
                                    [float(x) for x in ratings[match.id][0]['elo']], 
                                    [float(x) for x in ratings[match.id][1]['elo']]
                                )
        correctly_predicited[match.id] = 1 if \
                    match.score1 > match.score2 and \
                    predictions[match.id][0] > predictions[match.id][1] or \
                    match.score1 < match.score2 and \
                    predictions[match.id][0] < predictions[match.id][1] \
                    else 0
                     
        
    return render(
        request,
        'Soccer/Match/index.html',
        {
            'matches': matches,
            'ratings': ratings,
            'predictions': predictions,
            'cpredicted': correctly_predicited
        }
    )

# def matches(request):
#     # df = pd.read_csv(staticfiles_storage.url('soccer/Orlovna.csv'))

#     # matches = Match.objects.all().order_by('-pk')
#     # matches_ordered = Match.objects.all().order_by('pk')
#     ratings = f.get_all_ratings_at()
    
#     for match_id, rs in ratings.items():
#         elo, ts, mse = dict(rs[0]), dict(rs[1]), dict(rs[2])
#         players = list(elo.keys())
#         match_rs = []

#         for player in players:
#             pl = Player.objects.get(name=player)
#             rating = Rating()
#             rating.player = pl
#             rating.elo = elo[player]
#             rating.mu = ts[player]['mu']
#             rating.sigma = ts[player]['sigma']
#             rating.mse = mse[player]
#             rating.save()
#             match_rs.append(rating)

#         m = Match.objects.get(pk=match_id)
#         m.rating.set(match_rs)
#         m.save()

#     return render(
#         request,
#         'Soccer/Match/index.html',
#         {
#             # 'matches': matches,
#             # 'elo': ratings
#         }
#     )

def match_new(request):
    if request.method == 'POST':
        form = MatchNewForm(request.POST)

        if form.is_valid():
            match = Match()

            match.season = form.cleaned_data['season']
            match.session = form.cleaned_data['session']
           
            match.score1 = form.cleaned_data['score1']
            match.score2 = form.cleaned_data['score2']

            match.save()
            
            team1, team2 = [], []

            for player_id in form.cleaned_data['team1']:
                team1.append(Player.objects.get(pk=player_id))
                
            for player_id in form.cleaned_data['team2']:
                team2.append(Player.objects.get(pk=player_id))

            match.team1.set(team1)
            match.team2.set(team2)

            match.save()

        return redirect('matches')

    form = MatchNewForm()

    return render(
        request, 
        'Soccer/Match/new.html', 
        {'form': form}
    )

def match_delete(request, match_id):
    match = Match.objects.get(id=match_id)
    match.delete()

    return redirect('matches')

def players(request):
    players = Player.objects.all()
    elo, ts, mse = f.get_all_ratings()
    games = f.get_all_games()
    w_streaks, l_streaks = f.get_longest_winning_streaks(), f.get_longest_losing_streaks()

    streaks = {
        pl.name: (w_streaks[pl.name], l_streaks[pl.name]) 
        for pl in players
    }

    return render(
        request,
        'Soccer/Player/index.html',
        {
            'players': players,
            'elo': dict(elo),
            'ts': dict(ts),
            'games': games,
            'streaks': streaks
        }
    )

def player_detail(request, player_name):
    player = Player.objects.get(name=player_name)
    ratings = f.get_player(player.name)
    games = f.get_games(player.name)
    w_streak, l_streak = f.get_streaks(player.name)
    lw_streak, ll_streak = f.get_longest_streaks(player.name)

    ratings = (
        ratings[0],
        {
            'mu': [r.mu for _, r in ratings[1].items()],
            'sigma': [r.sigma for _, r in ratings[1].items()],
            'cse': [r.mu-3*r.sigma for _, r in ratings[1].items()]
        }
    )

    rating_development = f.get_rating_development_plot(ratings)
    trueskill_development = f.get_trueskill_development_plot(ratings[1])

    return render(
        request,
        'Soccer/Player/detail.html',
        {
            'player': player,
            'ratings': ratings,
            'games': games,
            'w_streak': w_streak,
            'l_streak': l_streak,
            'lw_streak': lw_streak,
            'll_streak': ll_streak,
            'rating_development': rating_development,
            'trueskill_development': trueskill_development
        }
    )

def player_new(request):
    return render(
        request,
        'Soccer/Player/new.html'
    )