import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Instrument(models.Model):
    """
    Instrument creates the table for the registered instruments.

    Fields:
      instrument_type: CharField(200) NOT NULL  ->  Type of the instrument (Drums, Marimba,...)
      instrument_brand: CharField(500)  ->  Brand of the instrument
      instrument_description: CharField(200)  ->  Description of the instrument
      instrument_date_bought: CharField(200)  ->  The date the instrument has been bought
      instrument_price: CharField(200)  ->  Price of the instrument
      instrument_store: CharField(200)  ->  Store where it has been bought
    """
    instrument_type = models.CharField(max_length=200, null=False)
    instrument_brand = models.CharField(max_length=200, blank=True)
    instrument_description = models.CharField(max_length=200, blank=True)
    instrument_date_bought = models.DateTimeField(blank=True)
    instrument_price = models.FloatField(default=0, blank=True)
    instrument_store = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "Instrument: " + self.instrument_type \
               + "( " + self.instrument_brand + ")"


class Reference(models.Model):
    """
    Reference creates the table for references of exercise.
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
    Exercise creates the table for single exercises.

    Fields:
      exercise_name: CharField(200) NOT NULL -> Name of the exercise
      exercise_added: DateTimeField() -> When the exercise has been added
      exercise_reference: ForeignKey(Reference) -> what is the reference of the exercise
    """
    exercise_name = models.CharField(max_length=200, null=False)
    exercise_added = models.DateTimeField('Date exercise added')
    exercise_reference = models.ForeignKey(Reference, on_delete=models.CASCADE)

    def __str__(self):
        return self.exercise_name

    def was_added_recently(self):
        """
        Returns True if the exercise has been added within the past 7 days.

        :return: Boolean
        """
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.exercise_added <= now

    was_added_recently.admin_order_field = 'exercise_added'
    was_added_recently.boolean = True
    was_added_recently.short_description = 'Added recently?'


class Execution(models.Model):
    """
    Execution holds all executions one has done. An execution is always consisting of a time start and end.

    Fields:
      execution_start: DateTimeField() -> Time started
      execution_end: DateTimeField() -> Time stopped
      execution_rating: int(default=5) -> How good was the performance.
                                          Range between 1, 10
      execution_tempo: int() -> Tempo executed (bpm)
                                Range > 0
      exercise: ForeignKey(Exercise) -> the exercise which has been executed / practiced
    """
    execution_start = models.DateTimeField('DateTime practice started')
    execution_end = models.DateTimeField('DateTime practice ended')
    execution_rating = models.IntegerField(default=5,
                                           validators=[MaxValueValidator(10),MinValueValidator(1)])
    execution_tempo = models.IntegerField(validators=[MinValueValidator(1)])
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    def __str__(self):
        return "Execution of " + str(self.exercise) + " on: " + str(self.execution_start)

    def was_executed_recently(self):
        """
        returns True for exercise executions that have been done recently (past 7 days).

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

    def day_of_the_year_executed(self):
        """
        Returns the day (1-365) in the year, on which the execution has been done

        :return: DateTime: Day of the year (1-365)
        """
        date = self.execution_start
        return str(date.strftime("%j"))

    was_executed_recently.admin_order_field = 'exercise_added'
    day_of_the_year_executed.admin_order_field = 'Day of the year'
    was_executed_recently.boolean = True


class PracticeList(models.Model):
    """
    PracticeList
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

