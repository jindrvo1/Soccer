from django import forms

from .models import Match, Player

class MatchNewForm(forms.Form):
    players = Player.objects.values_list('id', 'name')

    season = forms.IntegerField()
    session = forms.IntegerField()
    team1 = forms.MultipleChoiceField(
                choices = players,
                widget = forms.CheckboxSelectMultiple
            )
    team2 = forms.MultipleChoiceField(
                choices = players,
                widget  = forms.CheckboxSelectMultiple
            )
    score1 = forms.IntegerField()
    score2 = forms.IntegerField()
