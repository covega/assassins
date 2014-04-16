from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMessage

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

    # If viewer is an admin, render admin page
    try:
        admin_obj = Admin.objects.get(sunetid=sunetid)
        return admin(request, context, admin_obj)
    except Admin.DoesNotExist as e:
        pass

    # Get current player. If no player, ask if they want to play
    try:
        current_player = Player.objects.get(sunetid=sunetid)
        context['current_player'] = current_player
    except Player.DoesNotExist as e:
        return register_new_player(request, context, sunetid)

    # Get current player's dorm
    dorm = current_player.dorm

    # Game hasn't started yet
    if not dorm.game_started:
        return game_not_started(request, context)

    # Get list of dead and living players
    context['dead_players'] = Player.objects.filter(living=False, dorm=dorm)
    context['living_players'] = Player.objects.filter(living=True, dorm=dorm)

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
        if (game_over(current_player.dorm)):
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
    dorm_name = request.POST['dorm']
    dorm = Dorm.objects.get(name=dorm_name)

    newPlayer = Player(sunetid=sunetid, first_name=first_name, last_name = last_name, dorm=dorm)
    newPlayer.save()

    messages.success(request, 'Registration successful')

    return HttpResponseRedirect('/assassins')


def update_dorm_info(request):
    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponseRedirect('/')

    # Error out if poster is not an admin
    try:
        admin_obj = Admin.objects.get(sunetid=sunetid)
    except Admin.DoesNotExist as e:
        messages.error(request, "You're not an admin...")
        return HttpResponseRedirect('/')

    dorm = admin_obj.dorm

    if (request.POST['game_started'] == 'true'):
        dorm.game_started = True
    else:
        dorm.game_started = False

    dorm.save()
    
    messages.success(request, "Dorm info updated successfully")
    
    return HttpResponseRedirect('/assassins')


def assign_targets(request):
    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponseRedirect('/')

    # Error out if poster is not an admin
    try:
        admin_obj = Admin.objects.get(sunetid=sunetid)
    except Admin.DoesNotExist as e:
        messages.error(request, "You're not an admin...")
        return HttpResponseRedirect('/')

    dorm = admin_obj.dorm

    assassins.models.assign_targets(dorm)
    
    messages.success(request, "Targets assigned!")
    
    return HttpResponseRedirect('/assassins')


def send_email(request):
    # Get sunetid
    sunetid = get_sunetid(request)
    if sunetid is None:
        return HttpResponseRedirect('/')

    # Error out if poster is not an admin
    try:
        admin_obj = Admin.objects.get(sunetid=sunetid)
    except Admin.DoesNotExist as e:
        messages.error(request, "You're not an admin...")
        return HttpResponseRedirect('/')

    dorm = admin_obj.dorm

    recipients_type = request.GET['recipients']
    if recipients_type == "everyone":
        recipients = Player.objects.filter(dorm=dorm)
    elif recipients_type == "living":
        recipients = Player.objects.filter(dorm=dorm, living=True)
    elif recipients_type == "dead":
        recipients = Player.objects.filter(dorm=dorm, living=False)
    elif recipients_type == "specific":
        recipient_list = request.GET.getlist('recipient_list')
        recipients = Player.objects.filter(dorm=dorm, sunetid__in = recipient_list)
    else:
        messages.error(request, "Bad recipients choice. Recipients is %s" % recipients_type)
        return HttpResponseRedirect('/assassins')

    dest_addresses = [recip.sunetid + "@stanford.edu" for recip in recipients]
    subject_field = request.GET['subject_field']
    from_field = request.GET['from_field'] + " <%s>" % OUTGOING_MAIL_ADDRESS
    body = request.GET['body']

    #send_mail(subject_field, body, from_field, dest_addresses)
    email = EmailMessage(subject_field, body, from_field, 
                         to=[OUTGOING_MAIL_ADDRESS],
                         bcc=dest_addresses)
    email.send()

    messages.success(request, "Email sent!")
    return HttpResponseRedirect('/assassins')


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
    context['dorms'] = Dorm.objects.all()
    site = 'assassins/register_new_player.html'
    return render(request, site, context)

def game_not_started(request, context):
    site = 'assassins/game_not_started.html'
    return render(request, site, context)


def admin(request, context, admin):
    # Get sunetid
    sunetid = get_sunetid(request)

    dorm = admin.dorm

    context['dorm'] = dorm
    context['living_players'] = Player.objects.filter(living=True, dorm=dorm)
    context['dead_players'] = Player.objects.filter(living=False, dorm=dorm)
    context['all_players'] = Player.objects.filter(dorm=dorm)

    return render(request, 'assassins/admin.html', context)

