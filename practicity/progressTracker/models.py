import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Exercise(models.Model):
    """
    Exercise creates the table for single exercises.
    """
    exercise_name = models.CharField(max_length=200)
    exercise_add_date = models.DateTimeField('Date exercise added')
    exercise_executed = models.IntegerField(default=0)

    def __str__(self):
        return self.exercise_name

    def was_added_recently(self):
        return self.exercise_add_date >= timezone.now() - datetime.timedelta(days=1)


class PracticeSession(models.Model):
    """
    PracticeSessions creates the table for practice sessions. Meaning; A training workout
    """
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    practice_session_start = models.DateTimeField('DateTime practice started')
    practice_session_end = models.DateTimeField('DateTime practice ended')

    def __str__(self):
        return "Practice session on: " + str(self.practice_session_start)
