from django.contrib import admin

from .models import Player, Match, Rating

admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Rating)
