from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('team/', views.index, name="index"),
    path('team/login/',     views.team_login,   name="team_login"),
    path('team/logout/',    views.team_logout,  name='team_logout'),
    path('team/step-1/',    views.team_step_1,  name="team_step_1"),
    path('team/step-2/',    views.team_step_2,  name="team_step_2"),
    path('team/step-3/',    views.team_step_3,  name="team_step_3"),
    path('team/step-4/',    views.team_step_4,  name="team_step_4"),
    path('team/step-5/',    views.team_step_5,  name="team_step_5"),
    path('team/step-6/',    views.team_step_6,  name="team_step_6"),
    path('team/step-7/',    views.team_step_7,  name="team_step_7"),
]
