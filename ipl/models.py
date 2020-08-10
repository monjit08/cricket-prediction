from django.db import models

class Matches(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    city = models.TextField()
    date = models.DateField()
    team1 = models.TextField()
    team2 = models.TextField()
    toss_winner = models.TextField()
    toss_decision = models.TextField()
    result = models.TextField()
    dl_applied = models.IntegerField()
    winner = models.TextField()
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    venue = models.TextField()