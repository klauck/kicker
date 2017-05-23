from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse
from skills.models import GameResult, Player


def update_trueskills():
    last_update = Player.objects.aggregate(Max('trueskill_date_time'))['trueskill_date_time__max']
    print(last_update)
    if last_update:
        new_game_results = GameResult.objects.filter(date_time__gt=last_update).order_by('date_time')
    else:
    	new_game_results = GameResult.objects.order_by('date_time')
    print(new_game_results)


def trueskills(request):
    update_trueskills()
    players = Player.objects.all()
    return HttpResponse("These are the EPIC Trueskills: %d players" % len(players))

