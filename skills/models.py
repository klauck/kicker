from django.db import models

# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    trueskill_date_time = models.DateTimeField()
    trueskill_sigma = models.FloatField()
    trueskill_gamma = models.FloatField()

    def __str__(self):
        return('%s %s (%f)' % (self.first_name, self.last_name, self.trueskill()))
    
class GameResult(models.Model):
    winner_front = models.ForeignKey(Player, related_name='winner_front_game_results')
    winner_back = models.ForeignKey(Player, related_name='winner_back_game_results')
    loser_front = models.ForeignKey(Player, related_name='loser_front_game_results')
    loser_back = models.ForeignKey(Player, related_name='loser_back_game_results')
    # winner score is always 6
    loser_score = models.IntegerField()
    date_time = models.DateTimeField()