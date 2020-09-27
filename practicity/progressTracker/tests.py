import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Exercise, Execution


# Create your tests here.
def create_practice_session(session_start, days):
    """
    Create a practice session with the given session_start and session_end.

    :param session_start:
    :param session_end:
    :return:
    """
    time_start = timezone.now() + datetime.timedelta(days=days)
    time_end = timezone.now() + datetime.timedelta(days=days, hours=1)

    return Execution.objects.create(practice_session_start=time_start,
                                    practice_session_end=time_end)


class IndexViewTests(TestCase):
    def test_no_practice_sessions(self):
        """
        The index view shall still return code 200 even if no practiceSession exists
        """
        response = self.client.get(reverse('progressTracker:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No executions are available")
        self.assertQuerysetEqual(response.context['latest_execution_list'], [])


class ExerciseModelTest(TestCase):
    """
    ExerciseModelTest contains all tests for the database model Exercise
    """
    def test_was_created_recently_with_future_exercise(self):
        """
        was_added_recently() returns False for exercises whose date_added is in future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_exercise = Exercise(exercise_added=time)
        self.assertIs(future_exercise.was_added_recently(), False)

    def test_was_created_recently_with_old_exercise(self):
        """
        was_added_recently() returns False for exercises whose date_added is older than one
        week
        """
        time = timezone.now() - datetime.timedelta(days=7, seconds=1)
        old_exercise = Exercise(exercise_added=time)
        self.assertIs(old_exercise.was_added_recently(), False)

    def test_was_created_recently_with_recent_exercise(self):
        """
        was_added_recently() returns True for exercises whose date_added is created within the
        last 7 days
        """
        time = timezone.now() - datetime.timedelta(days=1)
        recent_exercise = Exercise(exercise_added=time)
        self.assertIs(recent_exercise.was_added_recently(), True)


class ExecutionModelTest(TestCase):
    """
    Unittests for model Execution
    """
    def test_was_executed_recently_with_recent_date(self):
        """
        was_executed_recently() should return true with recent date
        """
        time = timezone.now() - datetime.timedelta(days=1)
        current_exercise = Exercise(pk=1,
                                    exercise_name="test_exercise",
                                    exercise_added=timezone.now() - datetime.timedelta(days=7))
        recent_execution = Execution(execution_start=time,
                                     execution_end=time + datetime.timedelta(hours=1),
                                     execution_rating=2,
                                     execution_tempo=50,
                                     exercise=current_exercise)
        self.assertTrue(recent_execution.was_executed_recently())

    def test_was_executed_recently_with_old_date(self):
        """
        was_executed_recently() should return False with date older than 7 days
        """
        time = timezone.now() - datetime.timedelta(days=7, hours=1)
        current_exercise = Exercise(pk=1,
                                    exercise_name="test_exercise",
                                    exercise_added=timezone.now() - datetime.timedelta(days=7))
        recent_execution = Execution(execution_start=time,
                                     execution_end=time + datetime.timedelta(hours=1),
                                     execution_rating=2,
                                     execution_tempo=50,
                                     exercise=current_exercise)
        self.assertFalse(recent_execution.was_executed_recently())

    def test_duration_executed_with_start_end_time_equal(self):
        """
        duration_executed should return 0 days, 0 minutes and 0 seconds if the start and
        end time is the same value
        """
        time = timezone.now()
        current_exercise = Exercise(pk=1,
                                    exercise_name="test_exercise",
                                    exercise_added=timezone.now() - datetime.timedelta(days=7))
        recent_execution = Execution(execution_start=time,
                                     execution_end=time,
                                     execution_rating=2,
                                     execution_tempo=50,
                                     exercise=current_exercise)
        self.assertEqual(recent_execution.duration_executed(), timezone.timedelta(days=0, hours=0, seconds=0))

    def test_duration_executed_with_realistic_start_end_time(self):
        """
        duration_executed should return the correct value if the start and
        end time is valid
        """
        time = timezone.now()
        current_exercise = Exercise(pk=1,
                                    exercise_name="test_exercise",
                                    exercise_added=timezone.now() - datetime.timedelta(days=7))
        recent_execution = Execution(execution_start=time,
                                     execution_end=time + timezone.timedelta(hours=1),
                                     execution_rating=2,
                                     execution_tempo=50,
                                     exercise=current_exercise)

        self.assertEqual(recent_execution.duration_executed(), timezone.timedelta(hours=1))



