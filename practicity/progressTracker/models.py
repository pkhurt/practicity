from django.db import models


# Create your models here.
class Exercise(models.Model):
    """
    Exercise creates the table for single exercises.
    """
    exercise_name = models.CharField(max_length=200)
    exercise_add_date = models.DateField('Date exercise added')
    exercise_executed = models.IntegerField(default=0)


class PracticeSession(models.Model):
    """
    PracticeSessions creates the table for practice sessions. Meaning; A training workout
    """
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    practice_session_start = models.DateTimeField('DateTime practice started')
    practice_session_end = models.DateTimeField('DateTime practice ended')
