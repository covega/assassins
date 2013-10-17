from django.shortcuts import render
from django.http import HttpResponse

from assassins.models import Player

def index(request):
    temp_sunetid = 'gavilan'

    current_player = Player.objects.get(sunetid=temp_sunetid)
    context = {'current_player': current_player}
    return render(request, 'assassins/index.html', context)
