from django.shortcuts import render
from django.http import HttpResponse

from assassins.models import Player, Quote

# Sites
def index(request):
    context = {}

    temp_sunetid = 'gavilan'

    current_player = Player.objects.get(sunetid=temp_sunetid)
    context['current_player'] = current_player

    get_quote(context)

    if (current_player.living):
        site = 'assassins/living_player_home.html'
    else:
        site = 'assassins/dead_player_home.html'

    return render(request, site, context)

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


# Helper functions
def get_quote(context):
    # Get random quote
    quote = Quote.objects.order_by('?')[0]
    context['quote'] = quote
