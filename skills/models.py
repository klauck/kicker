from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return ('%s %s' % (self.first_name, self.last_name))

    def name(self):
        return ('%s %s' % (self.first_name, self.last_name))

    def initials(self):
        return self.first_name[0] + self.last_name[0]

    def change(self, old_mu, new_mu):
        return ('%s %s (%.2f (%+.2f))' % (self.first_name, self.last_name, new_mu, new_mu - old_mu))
    
class GameResult(models.Model):
    winner_front = models.ForeignKey(Player, related_name='winner_front_game_results')
    winner_back = models.ForeignKey(Player, related_name='winner_back_game_results')
    loser_front = models.ForeignKey(Player, related_name='loser_front_game_results')
    loser_back = models.ForeignKey(Player, related_name='loser_back_game_results')
    # winner score is always 6
    loser_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    date_time = models.DateTimeField()

    def __str__(self):
        return ('%s, %s : %s, %s    6:%d' % (self.winner_front.initials(), self.winner_back.initials(), \
                self.loser_front.initials(), self.loser_back.initials(), self.loser_score))

    def clean(self):
        if self.winner_front == self.winner_back or self.loser_front == self.loser_back:
            raise ValidationError('Players may not play with themselfes.')

        if self.winner_front == self.loser_front or self.winner_front == self.loser_back or \
                self.winner_back == self.loser_front or self.winner_back == self.loser_back:
            raise ValidationError('Players may not play against themselfes.')

class Season(models.Model):
    begin = models.DateField()
    end = models.DateField()

    def __str__(self):
        return 'Season %s - %s' % (self.begin, self.end)

    def clean(self):
        if self.begin > self.end:
            raise ValidationError('Begin date must be equal or smaller than end date.')
