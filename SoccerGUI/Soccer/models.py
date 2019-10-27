from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Rating(models.Model):
    player = models.ForeignKey(Player, on_delete="CASCADE", related_name="ratings")
    elo = models.DecimalField(decimal_places=10, max_digits=14, default=1200.0)
    mu = models.DecimalField(decimal_places=10, max_digits=12, default=25.0)
    sigma = models.DecimalField(decimal_places=10, max_digits=11, default=25.0/3)
    mse = models.DecimalField(decimal_places=10, max_digits=11, default=0.5)

class Match(models.Model):
    season = models.IntegerField()
    session = models.IntegerField()
    team1 = models.ManyToManyField(Player, related_name="team1")
    team2 = models.ManyToManyField(Player, related_name="team2")
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    rating = models.ManyToManyField(Rating, related_name="match")

    def __str__(self):
        team1 = ", ".join([pl.name for pl in self.team1.all()])
        team2 = ", ".join([pl.name for pl in self.team2.all()])
        return f"{self.season}.{self.session}: {team1} vs {team2}"
