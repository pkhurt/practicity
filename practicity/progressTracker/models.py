import datetime

from django.db import models
from django.utils import timezone


class Reference(models.Model):
    """
    ExerciseReference creates the table for references of exercise.
    References of exercise can be books, magazines, DVDs,... If no reference exists that is okay for an exercise

    Fields:
      reference_name: CharField(200) NOT NULL  ->  Name of the reference
      reference_ISBN: CharField(500)  ->  ISBN of the reference, if exist
      reference_author: CharField(200)  ->  Author of the reference, if exist
    """
    reference_name = models.CharField(max_length=200, null=False)
    reference_ISBN = models.CharField(max_length=500, null=True, blank=True)
    reference_author = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.reference_name + " (" + self.reference_author + ")"


class Exercise(models.Model):
    """
    Todo: Description
    Exercise creates the table for single exercises.
    """
    exercise_name = models.CharField(max_length=200, null=False)
    exercise_added = models.DateTimeField('Date exercise added')
    exercise_reference = models.ForeignKey(Reference, on_delete=models.CASCADE)

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
    execution_tempo = models.IntegerField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return "Execution of " + str(self.exercise) + " on: " + str(self.execution_start)

    def was_executed_recently(self):
        """
        returns true for exercise executions that have been done recently (past 7 days).
        :return:
            Boolean: True -> executed within last 7 days
                     False -> Not
        """
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.execution_start <= now

    def duration_executed(self):
        """
        returns the duration of the exercise execution
        :return:
            DateTime: Duration of execution
        """
        return self.execution_end - self.execution_start

    def date_of_execution_formatted(self):
        """
        Returns the date of an execution in a more readable and beautiful format
        :return:
            DateTime: Format -> Monday, 01. September 2020
        """
        date = self.execution_start
        return date.strftime("%A") + ", " + \
               date.strftime("%d") + ". " + \
               date.strftime("%B") + " " + \
               date.strftime("%Y")

    was_executed_recently.admin_order_field = 'exercise_added'
    was_executed_recently.boolean = True


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

