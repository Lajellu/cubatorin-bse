from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('team/', views.index, name="index"),
    path('team/login/',     views.team_login,   name="team_login"),
    path('team/logout/',    views.team_logout,  name='team_logout'),
    path('team/step-1/',    views.team_step_1,  name="team_step_1"),
]