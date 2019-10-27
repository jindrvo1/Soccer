from django.urls import path

from . import views

urlpatterns = [
    path('matches', views.matches, name='matches'),
    path('match/add', views.match_new, name='match-new'),
    path('match/delete/<int:match_id>', views.match_delete, name='match-delete'),

    path('', views.players, name='players'),
    path('player/<str:player_name>', views.player_detail, name='player-detail'),
    path('player/add', views.player_new, name='player-new')
]