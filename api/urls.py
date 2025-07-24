from django.urls import path
from . import views

urlpatterns = [
    path('save_field/', views.save_field),
    path('suggest_focus_areas/', views.suggest_focus_areas),
    path('suggest_causes/', views.suggest_causes),
    
]