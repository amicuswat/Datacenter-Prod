from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.storage_information_view import get_delta
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone
from django.utils.timezone import localtime



def is_strange(delay, strange_interval):
    total_seconds = delay.total_seconds()
    minutes = int(total_seconds // 60)
    
    return minutes >= strange_interval


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    
    visits = Visit.objects.filter(passcard=passcard)

    strange_interval = 60

    this_passcard_visits = []

    for visit in visits:        
        delay = get_delta(visit.entered_at, visit.leaved_at)
        
        is_strange_ = is_strange(delay, strange_interval)

        visit_details = {
            'entered_at': visit.entered_at,
            'duration': delay,
            'is_strange': is_strange_,
        }
        
        this_passcard_visits.append(visit_details)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
