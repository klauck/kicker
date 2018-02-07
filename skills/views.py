from django.db.models import Count, Min
from django.shortcuts import render, redirect
from django.http import HttpResponse
from skills.models import GameResult, Player, Season
import datetime
import trueskill


def recalculate_trueskills(game_results):
    players = Player.objects.all()
    players_ratings = {p.id: trueskill.Rating(mu=25.000, sigma=8.333) for p in players}

    latest_games = []
    for result in game_results:
        winner_front = result.winner_front
        winner_back = result.winner_back
        loser_front = result.loser_front
        loser_back = result.loser_back

        winner_front_rating = players_ratings[winner_front.id]
        winner_back_rating = players_ratings[winner_back.id]
        loser_front_rating = players_ratings[loser_front.id]
        loser_back_rating = players_ratings[loser_back.id]

        (winner_front_new_rating, winner_back_new_rating), (loser_front_new_rating, loser_back_new_rating) = \
            trueskill.rate([[winner_front_rating, winner_back_rating], [loser_front_rating, loser_back_rating]], ranks=[0, 1])

        latest_games.append({
                'winner_front': winner_front.change(winner_front_rating.mu, winner_front_new_rating.mu),
                'winner_back': winner_back.change(winner_back_rating.mu, winner_back_new_rating.mu),
                'loser_front': loser_front.change(loser_front_rating.mu, loser_front_new_rating.mu),
                'loser_back': loser_back.change(loser_back_rating.mu, loser_back_new_rating.mu),
                'result': '6:%d' % result.loser_score, 'date': result.date_time})

        players_ratings[winner_front.id] = winner_front_new_rating
        players_ratings[winner_back.id] = winner_back_new_rating
        players_ratings[loser_front.id] = loser_front_new_rating
        players_ratings[loser_back.id] = loser_back_new_rating

    return latest_games, players_ratings

def current_season(request):
    today = datetime.datetime.today().date()
    current_seasons = Season.objects.filter(begin__lte=today, end__gte=today)
    if len(current_seasons) == 1:
        return redirect('table', begin_date_str=str(current_seasons[0].begin), end_date_str=str(today))
    first_game_date = GameResult.objects.aggregate(Min('date_time'))
    return redirect('table', begin_date_str=str(first_game_date['date_time__min'].date()), end_date_str=str(today))



def table(request, begin_date_str, end_date_str):
    begin_date = datetime.datetime.strptime(begin_date_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    date_time_filter = {'date_time__date__gte': begin_date, 'date_time__date__lte': end_date}

    game_results = GameResult.objects.filter(**date_time_filter).order_by('date_time')
    latest_games, players_ratings = recalculate_trueskills(game_results)
    table = []
    for player in Player.objects.all():
        rating = players_ratings[player.id]
        won_games = len(player.winner_front_game_results.filter(**date_time_filter)) \
                + len(player.winner_back_game_results.filter(**date_time_filter))
        lost_games = len(player.loser_front_game_results.filter(**date_time_filter)) \
                + len(player.loser_back_game_results.filter(**date_time_filter))
        if won_games == 0 and lost_games ==0:
            continue
        table.append({'name': player.name(), 'id': player.pk, 'num_games': won_games + lost_games, \
                'points': '%d:%d' % (won_games, lost_games), 'mu': rating.mu, 'sigma': rating.sigma, \
                'rank': rating.mu - 3 * rating.sigma})
    if len(latest_games) > 10:
        latest_games = latest_games[-10:]
    return render(request, 'skills/table.html', context={'begin_date_str': begin_date_str, 'end_date_str': end_date_str,
        'table': sorted(table, key=lambda k: -k['mu']), 'latest_games': latest_games[::-1]})


def player(request, player_id, begin_date_str, end_date_str):
    begin_date = datetime.datetime.strptime(begin_date_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    date_time_filter = {'date_time__date__gte': begin_date, 'date_time__date__lte': end_date}

    player = Player.objects.get(pk=int(player_id))

    winner_front_partners = player.winner_front_game_results.filter(**date_time_filter).values('winner_back').annotate(Count('winner_back'))
    winner_back_partners = player.winner_back_game_results.filter(**date_time_filter).values('winner_front').annotate(Count('winner_front'))
    loser_front_partners = player.loser_front_game_results.filter(**date_time_filter).values('loser_back').annotate(Count('loser_back'))
    loser_back_partners = player.loser_back_game_results.filter(**date_time_filter).values('loser_front').annotate(Count('loser_front'))

    player_partners = {}
    for partner in winner_front_partners:
        partner_id = partner['winner_back']
        if partner_id not in player_partners:
            player_partners[partner_id] = [0, 0, 0, 0]
        player_partners[partner_id][0] = partner['winner_back__count']

    for partner in winner_back_partners:
        partner_id = partner['winner_front']
        if partner_id not in player_partners:
            player_partners[partner_id] = [0, 0, 0, 0]
        player_partners[partner_id][1] = partner['winner_front__count']

    for partner in loser_front_partners:
        partner_id = partner['loser_back']
        if partner_id not in player_partners:
            player_partners[partner_id] = [0, 0, 0, 0]
        player_partners[partner_id][2] = partner['loser_back__count']

    for partner in loser_back_partners:
        partner_id = partner['loser_front']
        if partner_id not in player_partners:
            player_partners[partner_id] = [0, 0, 0, 0]
        player_partners[partner_id][3] = partner['loser_front__count']

    table = []
    for partner in player_partners:
        table.append({'name': Player.objects.get(pk=partner).name(), 'id': partner, 'num_games': sum(player_partners[partner]),
                'points_front': '%d:%d' % (player_partners[partner][0], player_partners[partner][2]),
                'points_back': '%d:%d' % (player_partners[partner][1], player_partners[partner][3])})

    return render(request, 'skills/player.html', context={'begin_date_str': begin_date_str, 'end_date_str': end_date_str,
        'table': sorted(table, key=lambda k: -k['num_games']), 'name': player.name()})
