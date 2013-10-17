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

    return render(request, 'assassins/index.html', context)

def kill(request):
    context = {}

    temp_sunetid = 'gavilan'

    current_player = Player.objects.get(sunetid=temp_sunetid)
    context['current_player'] = current_player

    get_quote(context)

    return render(request, 'assassins/kill.html', context)



# Helper functions
def get_quote(context):
    # Get random quote
    quote = Quote.objects.order_by('?')[0]
    context['quote'] = quote
