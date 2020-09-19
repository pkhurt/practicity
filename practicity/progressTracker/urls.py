from django.urls import path

from . import views

app_name = 'progressTracker'
urlpatterns = [
    # ex: /progressTracker
    path('', views.index, name='index'),
    path('session_detail/<int:practice_session_id>/', views.session_detail, name='session_detail'),
    path('exercise_detail/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),  # generic view
    path('session_history/', views.SessionHistoryView.as_view(), name='session_history'),  # generic view
    path('exercise_execution/<int:exercise_id>/', views.exercise_execution, name='exercise_execution'),
]