from django import forms


class ExecutionForm(forms.Form):
    """
    ExecutionForm holds the fields of the exercise execution form which is needed
    on any template to track the execution of an exercise
    """
    exercise = forms.CharField(label="Exercise", max_length=100)
    start = forms.CharField(label="Start time", max_length=100)
    end = forms.CharField(label="End time", max_length=100)
    rating = forms.CharField(label="Rating", max_length=100)
    tempo = forms.CharField(label="Tempo", max_length=100)
    timer = forms.CharField(label="Timer", disabled=True)
