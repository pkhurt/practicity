from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Exercise, PracticeSession


# Create your views here.
def index(request):
    latest_session_list = PracticeSession.objects.order_by('-practice_session_start')[:5]
    exercise_list = Exercise.objects.all()

    context = {
        'latest_session_list': latest_session_list,
        'exercise_list': exercise_list,
    }

    return render(request, 'progressTracker/index.html', context)


def session_detail(request, practice_session_id):
    practice_session = get_object_or_404(PracticeSession, pk=practice_session_id)
    return render(request, 'progressTracker/session_detail.html', {'practice_session': practice_session})


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    return render(request, 'progressTracker/exercise_detail.html', {'exercise': exercise})


def session_history(request):
    response = "You can see your session history here"
    return HttpResponse(response)