from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

import assassins.settings
from assassins.models import *
from assassins.utils import *

from addison_encrypt import decrypt

import os

REDIRECT_SITE_URL = "/"

# Sites
def index(request):
    context = {}

    # Load morbid quote
    context['quote'] = get_quote()

    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponseRedirect('/')

    # Get current player. If no player, ask if they want to play
    try:
        current_player = Player.objects.get(sunetid=sunetid)
        context['current_player'] = current_player
    except Player.DoesNotExist as e:
        return register_new_player(request, context, sunetid)

    # Game hasn't started yet
    if not assassins.settings.GAME_STARTED:
        return game_not_started(request, context)

    # Get list of dead and living players
    context['dead_players'] = Player.objects.filter(living=False)
    context['living_players'] = Player.objects.filter(living=True)

    # Game started, player still alive
    if (current_player.living):
        return living_player_home(request, context)
    # Player died
    else:
        return dead_player_home(request, context)


def kill(request):
    context = {}

    context['quote'] = get_quote()

    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponseRedirect('/')

    current_player = Player.objects.get(sunetid=sunetid)
    context['current_player'] = current_player

    return render(request, 'assassins/kill.html', context)


def confirm_kill(request):
    context = {}

    # Get quote
    context['quote'] = get_quote()

    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponseRedirect('/')

    # Get current player
    current_player = Player.objects.get(sunetid=sunetid)
    context['current_player'] = current_player

    # Get details of kill
    details = request.POST['details']

    # Only kill target if the submitted target matches the player's assigned
    # target. (These can be put out of sync if the user clicks "Confirm kill"
    # twice. The second time, the form will reflect a different target than
    # the player's assigned target)
    target_sunetid = request.POST['target']
    if target_sunetid == current_player.target.sunetid:
        current_player.kill_target(details)

        # Check if the game ended
        if (game_over()):
            return render(request, 'assassins/winner.html', context)

    messages.success(request, 'You have been assigned your new target. Good luck.')

    #return render(request, 'assassins/confirm_kill.html', context)
    return HttpResponseRedirect('/assassins')


def submit_registration(request):
    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponseRedirect('/')

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    newPlayer = Player(sunetid=sunetid, first_name=first_name, last_name = last_name)
    newPlayer.save()

    messages.success(request, 'Registration successful')

    return HttpResponseRedirect('/assassins')


def status(request):
    context = {}

    # Load morbid quote
    context['quote'] = get_quote()

    # Load living players
    context['game_ring'] = game_ring_in_order()

    # Load dead players
    context['dead_players'] = Player.objects.filter(living=False)

    return render(request, 'assassins/status.html', context)


'''
Views Index may redirect to
'''
def living_player_home(request, context):
    site = 'assassins/living_player_home.html'
    return render(request, site, context)


def dead_player_home(request, context):
    site = 'assassins/dead_player_home.html'
    return render(request, site, context)


def register_new_player(request, context, sunetid):
    context['first_name'] = request.GET['first']
    context['last_name'] = request.GET['last']
    site = 'assassins/register_new_player.html'
    return render(request, site, context)

def game_not_started(request, context):
    site = 'assassins/game_not_started.html'
    return render(request, site, context)



