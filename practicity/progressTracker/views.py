from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
from django.views import generic
from django.db import IntegrityError

import datetime

import plotly.graph_objs as go
from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar

from .models import Exercise, Execution, Reference, Instrument, Category, ExerciseCategory

from .forms import ExecutionForm


def index(request):
    """
    View: index
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
    execution_list = Execution.objects.all().order_by('execution_start')
    exercise_list = Exercise.objects.all()

    # The total summed up time of execution
    total_execution_time = datetime.timedelta(days=0, hours=0, minutes=0)
    for execution in execution_list:
        total_execution_time += execution.duration_executed()

    # Plot data
    x_plot_data = []
    y_plot_data = []
    duration = datetime.timedelta()
    for execution in execution_list:
        x_plot_data.append(execution.execution_start.strftime('%Y-%m-%d %H'))
        duration += execution.duration_executed()
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
            try:
                execution = Execution(execution_start=request.POST['start'],
                                      execution_end=request.POST['end'],
                                      execution_rating=request.POST['rating'],
                                      execution_tempo=request.POST['tempo'],
                                      exercise_id=request.POST["exercise"])
                execution.save()
                return HttpResponseRedirect('/exercises/')
            except IntegrityError as e:
                return render('progressTracker/exercises.html', {"message": e})

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
    executions_list = Execution.objects.all().order_by('execution_start')
    instrument_list = Instrument.objects.all()
    category_list = Category.objects.all()
    exercise_category_list = ExerciseCategory.objects.all()

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

    # PLOT: practice bpm history
    fig = go.Figure()
    # add all the traces
    for exercise in exercises_list:
        x_plot_data = []
        y_plot_data = []
        this_executions = Execution.objects.filter(exercise=exercise)

        for execution in this_executions:
            x_plot_data.append(str(execution.execution_start))
            y_plot_data.append(int(execution.execution_tempo))

        fig.add_trace(go.Scatter(x=x_plot_data, y=y_plot_data,
                                 mode='lines+markers', name=exercise.exercise_name,
                                 opacity=0.8))

    fig.update_traces(marker_line_width=1, marker_size=10)
    fig.update_layout(title='Practice BPM over time',
                      paper_bgcolor='rgba( 255, 255 , 255, 0.4 )')
    plot_bpm = plot(fig, output_type='div')

    # PLOT: practice rating history
    fig = go.Figure()
    # add all the traces
    for exercise in exercises_list:
        x_plot_data = []
        y_plot_data = []
        this_executions = Execution.objects.filter(exercise=exercise).order_by('execution_start')

        for execution in this_executions:
            x_plot_data.append(str(execution.execution_start))
            y_plot_data.append(int(execution.execution_rating))

        fig.add_trace(go.Scatter(x=x_plot_data, y=y_plot_data,
                                 mode='lines+markers', name=exercise.exercise_name,
                                 opacity=0.8))

    fig.update_traces(marker_line_width=1, marker_size=10)
    fig.update_layout(title='Practice Rating over time',
                      paper_bgcolor='rgba( 255, 255 , 255, 0.4 )')
    plot_rating = plot(fig, output_type='div')

    # PLOT: practice rating history
    fig = go.Figure()
    # add all the traces
    for instrument in instrument_list:
        x_plot_data = []
        y_plot_data = []
        this_executions = Execution.objects.filter(instrument=instrument)

        instrument_num_executions = 0
        for execution in this_executions:
            instrument_num_executions += 1

        x_plot_data.append(instrument.instrument_brand)
        y_plot_data.append(instrument_num_executions)

        fig.add_trace(go.Bar(x=x_plot_data, y=y_plot_data,
                             name=instrument.instrument_brand,
                             opacity=0.8))

    fig.update_layout(title='Instrument practiced',
                      paper_bgcolor='rgba( 255, 255 , 255, 0.4 )')
    plot_instrument_practiced = plot(fig, output_type='div')


    # PLOT number of exercises in category
    fig = go.Figure()
    # add all the traces
    for category in category_list:
        x_plot_data = []
        y_plot_data = []
        this_exercises = ExerciseCategory.objects.filter(category=category)

        exercises_in_category = 0
        for exercise in this_exercises:
            exercises_in_category += 1

        x_plot_data.append(category.category_name)
        y_plot_data.append(exercises_in_category)

        fig.add_trace(go.Bar(x=x_plot_data, y=y_plot_data,
                             name=category.category_name,
                             opacity=0.8))

    fig.update_layout(title='Number of exercises in category',
                      paper_bgcolor='rgba( 255, 255 , 255, 0.4 )')
    plot_exercises_in_category = plot(fig, output_type='div')

    context = {
        "exercises_list": exercises_list,
        "executions_list": executions_list,
        "plot_execution_time": plot_execution_time,
        "plot_bpm": plot_bpm,
        "plot_rating": plot_rating,
        "plot_instrument_practiced": plot_instrument_practiced,
        "plot_exercises_in_category": plot_exercises_in_category,
    }

    return render(request, template_name, context)
