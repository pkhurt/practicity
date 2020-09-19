from django.shortcuts import render, get_object_or_404, get_list_or_404
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
    exercise_list = Exercise.objects.filter(practice_session=practice_session_id)
    context = {
        'practice_session': practice_session,
        'exercise_list': exercise_list,
    }
    return render(request, 'progressTracker/session_detail.html', context)


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    return render(request, 'progressTracker/exercise_detail.html', {'exercise': exercise})


def session_history(request):
    response = "You can see your session history here"
    return HttpResponse(response)


def exercise_execution(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.POST['execution'] == 'Executed':
        exercise.exercise_executed += 1
        exercise.save()
        return HttpResponse("You have successfully executed %s: Total now: %s " %
                            (exercise.exercise_name, str(exercise.exercise_executed)))
    else:
        return HttpResponse("You did not execute %s " % exercise.exercise_name)


