from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
from django.views import generic
import datetime

from plotly.offline import plot
from plotly.graph_objs import Scatter

from .models import Exercise, Execution, Reference

from .forms import ExecutionForm


def index(request):
    """
    View: indexs
    This view displays the index page of the progressTracker; "/progressTracker/".
    The display shows the latest execution list and the stored exercises.

    :return: context {
                latest_execution_list
                exercise_list
                form
                plot_div }
    """
    template_name = 'index.html'

    latest_execution_list = Execution.objects.filter(
        execution_start__lte=timezone.now()).order_by('-execution_start')[:5]
    execution_list = Execution.objects.all()
    exercise_list = Exercise.objects.all()

    # The total summed up time of execution
    total_execution_time = datetime.timedelta(days=0, hours=0, minutes=0)
    for execution in execution_list:
        total_execution_time += execution.duration_executed()

    # Plot data
    x_plot_data = []
    y_plot_data = []
    for execution in execution_list:
        x_plot_data.append(str(execution.execution_start))
        y_plot_data.append(str(execution.duration_executed()))

    plot_div = plot([Scatter(x=x_plot_data, y=y_plot_data,
                             mode='lines', name='test',
                             opacity=0.8, marker_color='green')],
                    output_type='div')

    # Get execution form
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
                                  exercise_id=request.POST["exercise"],
                                  instrument_id=request.POST["instrument"])
            execution.save()
            return HttpResponseRedirect('/progressTracker/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ExecutionForm()

    context = {
        'latest_execution_list': latest_execution_list,
        'exercise_list': exercise_list,
        'form': form,
        'plot_div': plot_div,
        'total_execution_time': total_execution_time,
    }

    return render(request, 'progressTracker/' + template_name, context)


def exercises_view(request):
    """
    The exercises_view shows all registered exercises.
    It also contains the availability to execute an exercise via a form module.

    table: Exercises
    template: exercises.html
    :return: Renders to: /progressTracker/exercises/
    """
    exercise_list = Exercise.objects.all()

    # get exercise execution form
    # Get execution form
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
            return HttpResponseRedirect('/exercises/')
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
    """
    The generic ExerciseDetailView shows the details of a specific exercise.

    table: Exercises
    template: exercise_detail.html
    :return: Renders to: /progressTracker/exercises/<int: Exercise.ID>
    """
    model = Exercise
    template_name = 'progressTracker/exercise_detail.html'


class ReferenceView(generic.ListView):
    """
    The generic ExerciseReferenceView shows the full list of registered references.

    table: Exercises
    template: exercise_detail.html
    :return: Renders to: /progressTracker/exercises/<int: Exercise.ID>
    """
    model = Reference
    context_object_name = "exercise_reference_list"
    template_name = 'progressTracker/exercise_references.html'


def exercise_execution(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.POST['start']:
        return HttpResponse("Nice! Time Submitted! %s " % request.POST['start'])

    return HttpResponse("Nice! You executed exercise %s " % exercise.exercise_name)


def statistics_view(request):
    """
    This view shall show all global statistics of the practices and executions
    :param request:
    :return:
    """
    exercises_list = Exercise.objects.all()
    executions_list = Execution.objects.all()

    template_name = "progressTracker/statistics.html"

    # Executions plot data
    x_plot_data = []
    y_plot_data = []
    for execution in executions_list:
        x_plot_data.append(str(execution.execution_start))
        y_plot_data.append(str(execution.duration_executed()))

    plot_execution_time = plot([Scatter(x=x_plot_data, y=y_plot_data,
                                        mode='lines', name='test',
                                        opacity=0.8, marker_color='green')],
                                        output_type='div')

    context = {
        "exercises_list": exercises_list,
        "executions_list": executions_list,
        "plot_execution_time": plot_execution_time,
    }

    return render(request, template_name, context)
