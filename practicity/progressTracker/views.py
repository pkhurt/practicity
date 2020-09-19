from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Exercise, PracticeSession


# Create your views here.
def index(request):
    latest_session_list = PracticeSession.objects.order_by('-practice_session_start')[:5]
    template = loader.get_template('progressTracker/index.html')
    context = {
        'latest_session_list': latest_session_list,
    }
    return HttpResponse(template.render(context, request))


def session_detail(request, practice_session_id):
    return HttpResponse("you are looking at the details of Practice Session id %s" % practice_session_id)


def exercise_detail(request, exercise_id):
    response = "You are looking at the details of the exercise %s "
    return HttpResponse(response % exercise_id)


def session_history(request):
    response = "You can see your session history here"
    return HttpResponse(response)