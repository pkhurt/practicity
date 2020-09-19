import datetime

from django.db import models
from django.utils import timezone


class PracticeSession(models.Model):
    """
    PracticeSessions creates the table for practice sessions. Meaning; A training workout
    """
    practice_session_start = models.DateTimeField('DateTime practice started')
    practice_session_end = models.DateTimeField('DateTime practice ended')

    def __str__(self):
        return "Practice session on: " + str(self.practice_session_start)


# Create your models here.
class Exercise(models.Model):
    """
    Exercise creates the table for single exercises.
    """
    exercise_name = models.CharField(max_length=200)
    exercise_add_date = models.DateTimeField('Date exercise added')
    exercise_executed = models.IntegerField(default=0)
    practice_session = models.ForeignKey(PracticeSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.exercise_name

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.exercise_add_date <= now

#class PracticeSessionExercise(models.Model):
#    """
#    Solve n-n association between PracticeSession and Exercise
#    """
#    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
#    PracticeSession = models.ForeignKey(PracticeSession, on_delete=models.CASCADE)