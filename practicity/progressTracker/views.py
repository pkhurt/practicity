from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
from django.views import generic

from .models import Exercise, Execution

from .forms import ExecutionForm


# Form Post actions
def get_exercise(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = ExecutionForm(request.POST)
        # check if valid
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ExecutionForm()

    return render(request, 'exercise_execution.html', {'form', form})


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
    return render(request, 'progressTracker/exercises.html', context)


def exercises_view(request):
    exercise_list = Exercise.objects.all()
    # if this is a POST request we got feedback from the exercise execution form on the
    # template
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = ExecutionForm(request.POST)
        # check if valid
        if form.is_valid():
            # Write exercise execution into DB execution
            execution = Execution(execution_start=request.POST['start'],
                                  execution_end=request.POST['end'],
                                  execution_rating=request.POST['rating'],
                                  execution_tempo=request.POST['tempo'],
                                  exercise_id=request.POST["exercise"])
            execution.save()
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ExecutionForm()

    template_name = 'progressTracker/exercises.html'

    context = {
        'form': form,
        'exercise_list': exercise_list,
    }

    return render(request, template_name, context)



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

    if request.POST['start']:
        return HttpResponse("Nice! Time Submitted! %s " % request.POST['start'])

    return HttpResponse("Nice! You executed exercise %s " % exercise.exercise_name)

    # if request.POST['execution'] == 'Executed':
    #     exercise.exercise_executed += 1
    #     exercise.save()
    #     return HttpResponse("You have successfully executed %s: Total now: %s " %
    #                         (exercise.exercise_name, str(exercise.exercise_times_executed)))
    # else:
    #     return HttpResponse("You did not execute %s " % exercise.exercise_name)
    # context = {
    #     'exercise': exercise,
    # }
    # return render(request, 'progressTracker/exercise_execution.html', context)


