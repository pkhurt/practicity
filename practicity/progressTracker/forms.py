from django import forms
from .models import Instrument, Exercise

RATING_CHOICES =(
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
    ("6", "six"),
    ("7", "seven"),
    ("8", "eight"),
    ("9", "nine"),
    ("10", "ten"),
)


class ExecutionForm(forms.Form):
    """
    ExecutionForm holds the fields of the exercise execution form which is needed
    on any template to track the execution of an exercise
    """
    exercise = forms.ModelChoiceField(Exercise.objects.all())
    instrument = forms.ModelChoiceField(Instrument.objects.all())
    start = forms.DateTimeField(label="Start time")
    end = forms.DateTimeField(label="End time")
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    tempo = forms.CharField(label="Tempo", max_length=100)
    timer = forms.CharField(label="Timer", disabled=True, required=False)
    # TODO: add button to the form
