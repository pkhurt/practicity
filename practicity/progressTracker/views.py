from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Exercise, Execution


# Create your views here.
def index(request):
    latest_execution_list = Execution.objects.filter(
        execution_start__lte=timezone.now()).order_by('-execution_start')[:5]
    exercise_list = Exercise.objects.all()

    context = {
        'latest_session_list': latest_execution_list,
        'exercise_list': exercise_list,
    }

    return render(request, 'progressTracker/index.html', context)


def session_detail(request, practice_session_id):
    practice_session = get_object_or_404(Execution, pk=practice_session_id)
    exercise_list = Exercise.objects.filter(practice_session=practice_session_id)
    context = {
        'practice_session': practice_session,
        'exercise_list': exercise_list,
    }
    return render(request, 'progressTracker/session_detail.html', context)


class ExerciseDetailView(generic.DetailView):
    model = Exercise
    template_name = 'progressTracker/exercise_detail.html'


class SessionHistoryView(generic.ListView):
    """

    """
    model = Execution
    context_object_name = "practice_session_list"
    template_name = 'progressTracker/session_history.html'


def exercise_execution(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.POST['execution'] == 'Executed':
        exercise.exercise_executed += 1
        exercise.save()
        return HttpResponse("You have successfully executed %s: Total now: %s " %
                            (exercise.exercise_name, str(exercise.exercise_times_executed)))
    else:
        return HttpResponse("You did not execute %s " % exercise.exercise_name)


