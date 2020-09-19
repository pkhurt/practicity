from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello World. This is the Progress Tracker App.")


def session_detail(request, practice_session_id):
    return HttpResponse("you are looking at the details of Practice Session id %s" % practice_session_id)


def exercise_detail(request, exercise_id):
    response = "You are looking at the details of the exercise %s "
    return HttpResponse(response % exercise_id)


def session_history(request):
    response = "You can see your session history here"
    return HttpResponse(response)