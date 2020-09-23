from django.urls import path

from . import views

app_name = 'progressTracker'
urlpatterns = [
    # ex: /progressTracker
    path('', views.index, name='index'),
    path('exercise_detail/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),  # generic view
    path('exercise_execution/<int:exercise_id>/', views.exercise_execution, name='exercise_execution'),
    path('exercise_references/', views.ExerciseReferenceView.as_view(), name='exercise_references'),
    path('exercises', views.exercises_view, name='exercises'),
]