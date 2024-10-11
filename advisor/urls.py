from django.urls import path
from . import views

app_name = 'advisor'

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('advisees/', views.advisees, name='advisees'),
    path('advisee/<int:id>/', views.advisee, name='advisee'),
    path('article/<int:id>/feedback/<str:feedback>', views.article_feedback, name='article_feedback'),
    path('message/inbox/', views.message_inbox, name='message_inbox'),
    path('message/inbox/advisee/<int:advisee_id>/', views.message_advisee, name='message_advisee'),
    path('message/send/<int:advisee_id>/', views.message_send, name='message_send'),
    path('regenerate_advisee_topic_instructions/', views.regenerate_advisee_topic_instructions, name='regenerate_advisee_topic_instructions'),
    
]