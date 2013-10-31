from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

import assassins.settings
from assassins.models import Player, Quote, game_over
from assassins.utils import *

from addison_encrypt import decrypt

import os

REDIRECT_SITE_URL = "www.stanford.edu/~gavilan/cgi-bin/assassins.py"

# Sites
def index(request):
    context = {}

    # Load morbid quote
    context['quote'] = get_quote()

    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponse("No user found. Did you mean to navigate to %s" % REDIRECT_SITE_URL)

    # Get current player. If no player, ask if they want to play
    try:
        current_player = Player.objects.get(sunetid=sunetid)
        context['current_player'] = current_player
    except Player.DoesNotExist as e:
        return register_new_player(request, context, sunetid)

    # Game hasn't started yet
    if not assassins.settings.GAME_STARTED:
        return game_not_started(request, context)

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
        return HttpResponse("No user found. Did you mean to navigate to %s" % REDIRECT_SITE_URL)

    current_player = Player.objects.get(sunetid=sunetid)
    context['current_player'] = current_player

    return render(request, 'assassins/kill.html', context)


def confirm_kill(request):
    context = {}

    context['quote'] = get_quote()

    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponse("No user found. Did you mean to navigate to %s" % REDIRECT_SITE_URL)

    current_player = Player.objects.get(sunetid=sunetid)
    context['current_player'] = current_player

    details = request.POST['details']

    current_player.kill_target(details)

    if (game_over()):
        return render(request, 'assassins/winner.html', context)

    return render(request, 'assassins/confirm_kill.html', context)


def submit_registration(request):
    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponse("No user found. Did you mean to navigate to %s" % REDIRECT_SITE_URL)

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    newPlayer = Player(sunetid=sunetid, first_name=first_name, last_name = last_name)
    newPlayer.save()

    messages.success(request, 'Registration successful')

    return index(request)

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



