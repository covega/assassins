from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import assassins.settings

from assassins.models import Player, Quote

import os

REDIRECT_SITE_URL = "www.stanford.edu/~gavilan/assassins.py"

# Sites
def index(request):
    context = {}

    # Load morbid quote
    get_quote(context)

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

    temp_sunetid = 'gavilan'

    current_player = Player.objects.get(sunetid=temp_sunetid)
    context['current_player'] = current_player

    get_quote(context)

    return render(request, 'assassins/kill.html', context)


def confirm_kill(request):
    context = {}

    temp_sunetid = 'gavilan'

    current_player = Player.objects.get(sunetid=temp_sunetid)
    context['current_player'] = current_player

    get_quote(context)

    details = request.POST['details']

    current_player.kill_target(details)

    return render(request, 'assassins/confirm_kill.html', context)


def submit_registration(request):
    context = {}

    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponse("No user found. Did you mean to navigate to %s" % REDIRECT_SITE_URL)

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    newPlayer = Player(sunetid=sunetid, first_name=first_name, last_name = last_name, living=False)
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


'''
Helper functions
'''
def get_quote(context):
    # Get random quote
    quote = Quote.objects.order_by('?')[0]
    context['quote'] = quote

def get_sunetid(request):
    # URL string had encrypted sunetid in it
    if 'usr' in request.GET:
        # Get sunetid from URL
        encrypted_sunetid = request.GET.get('usr')

        # Decrypt it
        sunetid = decrypt_id(encrypted_sunetid)

        # Store it in the session
        request.session['usr'] = sunetid

        return sunetid

    # sunetid is saved in the session
    if 'usr' in request.session:
        return request.session['usr']

    # No sunetid found
    return None


def decrypt_id(encrypted_id):
    id_minus_padding = encrypted_id[:-10]
    sunetid = rot13(id_minus_padding)
    return sunetid


def rot13(s):
    chars = "abcdefghijklmnopqrstuvwxyz"
    trans = chars[13:]+chars[:13]
    rot_char = lambda c: trans[chars.find(c)] if chars.find(c)>-1 else c
    return ''.join( rot_char(c) for c in s ) 

'''
def get_encrypted_sunetid(request):
    # URL string had sunetid in it
    if 'usr' in request.GET:
        # Get sunetid from URL
        encrypted_sunetid = request.GET.get('usr')
        
        # Save sunetid in session
        request.session['usr'] = encrypted_sunetid
        
        return encrypted_sunetid

    # sunetid is saved in the session
    if 'usr' in request.session:
        return request.session['usr']

    # No sunetid found
    return None
'''
