import datetime

from django.db import models
from django.utils import timezone


class ExerciseReference(models.Model):
    """
    ExerciseReference creates the table for references of exercise.
    References of exercise can be books, magazines, DVDs,... If no reference exists that is okay for an exercise

    Fields:
      exercise_reference_name: CharField(200) NOT NULL  ->  Name of the reference
      exercise_reference_ISBN: CharField(500)  ->  ISBN of the reference, if exist
      exercise_reference_author: CharField(200)  ->  Author of the reference, if exist
    """
    exercise_reference_name = models.CharField(max_length=200, null=False)
    exercise_reference_ISBN = models.CharField(max_length=500, null=True, blank=True)
    exercise_reference_author = models.CharField(max_length=200, null=True, blank=True)


class Exercise(models.Model):
    """
    Todo: Description
    Exercise creates the table for single exercises.
    """
    exercise_name = models.CharField(max_length=200, null=False)
    exercise_added = models.DateTimeField('Date exercise added')
    exercise_times_executed = models.IntegerField(default=0)
    exercise_reference = models.ForeignKey(ExerciseReference, on_delete=models.CASCADE)

    def __str__(self):
        return self.exercise_name

    def was_added_recently(self):
        """
        Todo: Description
        :return: Boolean
        """
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.exercise_added <= now

    was_added_recently.admin_order_field = 'exercise_added'
    was_added_recently.boolean = True
    was_added_recently.short_description = 'Added recently?'


class Execution(models.Model):
    """
    Todo: Description
    PracticeSessions creates the table for practice sessions. Meaning; A training workout
    """
    execution_start = models.DateTimeField('DateTime practice started')
    execution_end = models.DateTimeField('DateTime practice ended')
    execution_rating = models.IntegerField(default=5)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return "Execution of " + str(self.exercise) + " on: " + str(self.execution_start)


class PracticeList(models.Model):
    """
    TODO: Description
    """
    practice_list_name = models.CharField(max_length=200, null=False)
    practice_list_created = models.DateTimeField('Date the list has been created.')


class ExercisePracticeList(models.Model):
    """
    Todo: Description
    """
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    practice_list = models.ForeignKey(PracticeList, on_delete=models.CASCADE)

