from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime

from datetime import datetime, timezone


def get_delta(start, finish):
    if not finish:
        finish = datetime.now(timezone.utc)
        
    return localtime(finish) - localtime(start)
    

def format_duration(delta):
    total_seconds = delta.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int((total_seconds % 3600) % 60)
    if hours < 10:
        hours = f'0{hours}'
    if minutes < 10:
        minutes = f'0{minutes}'
    if seconds < 10:
        seconds = f'0{seconds}'

    return f'{hours}:{minutes}:{seconds}'


def storage_information_view(request):
    
    active_visits = Visit.objects.filter(leaved_at__isnull=True)

    non_closed_visits = []

    for visit in active_visits:
        who_entered = visit.passcard.owner_name
        entered_at = localtime(visit.entered_at)
        delta = get_delta(visit.entered_at, visit.leaved_at)
        duration = format_duration(delta)
        
        non_closed_visits.append({
            'who_entered': who_entered,
            'entered_at': entered_at,
            'duration': duration,
        })

    context = {
        'non_closed_visits': non_closed_visits, 
    }
    return render(request, 'storage_information.html', context)
