from django.urls import path

from . import views

app_name = 'progressTracker'
urlpatterns = [
    # ex: /progressTracker
    path('', views.index, name='index'),
    # ex:
    path('session_detail/<int:practice_session_id>/', views.session_detail, name='session_detail'),
    path('exercise_detail/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('session_history/', views.session_history, name='session_history'),
]