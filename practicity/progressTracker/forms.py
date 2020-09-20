from django import forms


class ExecutionForm(forms.Form):
    exercise = forms.CharField(label="Exercise", max_length=100)
    start = forms.CharField(label="Start time", max_length=100)
    end = forms.CharField(label="End time", max_length=100)
    rating = forms.CharField(label="Rating", max_length=100)
    tempo = forms.CharField(label="Tempo", max_length=100)
