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
        self.assertContains(response, "No sessions are available")
        self.assertQuerysetEqual(response.context['latest_session_list'], [])


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

    def test_was_executed_recently(self):
        """

        """
        time = timezone.now() - datetime.timedelta(days=1)
        current_exercise = Exercise(pk=1,
                                    exercise_name="test_exercise",
                                    exercise_added=timezone.now() - datetime.timedelta(days=7))
        Execution.objects.create(execution_start=time,
                                 execution_end=time + datetime.timedelta(hours=1),
                                 execution_rating=2,
                                 execution_tempo=50,
                                 exercise=current_exercise)
        self.assertIs(current_exercise.was_practiced_recently(), True)


