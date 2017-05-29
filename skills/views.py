from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse
from skills.models import GameResult, Player
import trueskill


def update_trueskills():
    last_update = Player.objects.aggregate(Max('trueskill_date_time'))['trueskill_date_time__max']
    print(last_update)
    if last_update:
        new_game_results = GameResult.objects.filter(date_time__gt=last_update).order_by('date_time')
    else:
        new_game_results = GameResult.objects.order_by('date_time')
    print(new_game_results)
    for result in new_game_results:
        winner_front = result.winner_front
        winner_back = result.winner_back
        loser_front = result.loser_front
        loser_back = result.loser_back

        winner_front_rating = trueskill.Rating(mu=winner_front.trueskill_mu, sigma=winner_front.trueskill_sigma)
        winner_back_rating = trueskill.Rating(mu=winner_back.trueskill_mu, sigma=winner_back.trueskill_sigma)
        loser_front_rating = trueskill.Rating(mu=loser_front.trueskill_mu, sigma=loser_front.trueskill_sigma)
        loser_back_rating = trueskill.Rating(mu=loser_back.trueskill_mu, sigma=loser_back.trueskill_sigma)

        (new_winner_front_rating, new_winner_back_rating), (new_loser_front_rating, new_loser_back_rating) = \
            trueskill.rate([[winner_front_rating, winner_back_rating], [loser_front_rating, loser_back_rating]], ranks=[0, 1])

        winner_front.trueskill_mu = new_winner_front_rating.mu
        winner_front.trueskill_sigma = new_winner_front_rating.sigma
        winner_front.trueskill_date_time = result.date_time
        winner_front.save()

        winner_back.trueskill_mu = new_winner_back_rating.mu
        winner_back.trueskill_sigma = new_winner_back_rating.sigma
        winner_back.trueskill_date_time = result.date_time
        winner_back.save()

        loser_front.trueskill_mu = new_loser_front_rating.mu
        loser_front.trueskill_sigma = new_loser_front_rating.sigma
        loser_front.trueskill_date_time = result.date_time
        loser_front.save()

        loser_back.trueskill_mu = new_loser_back_rating.mu
        loser_back.trueskill_sigma = new_loser_back_rating.sigma
        loser_back.trueskill_date_time = result.date_time
        loser_back.save()

def trueskills(request):
    update_trueskills()
    players = Player.objects.all()
    return HttpResponse("These are the EPIC Trueskills: %d players" % len(players))

