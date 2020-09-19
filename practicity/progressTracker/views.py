from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Exercise, PracticeSession


# Create your views here.
def index(request):
    latest_session_list = PracticeSession.objects.order_by('-practice_session_start')[:5]

    context = {
        'latest_session_list': latest_session_list,
    }

    return render(request, 'progressTracker/index.html', context)


def session_detail(request, practice_session_id):
    practice_session = get_object_or_404(PracticeSession, pk=practice_session_id)
    return render(request, 'progressTracker/session_detail.html', {'practice_session': practice_session})


def exercise_detail(request, exercise_id):
    response = "You are looking at the details of the exercise %s "
    return HttpResponse(response % exercise_id)


def session_history(request):
    response = "You can see your session history here"
    return HttpResponse(response)