from django.urls import path
from . import views

urlpatterns = [
    path('save_field/', views.save_field),
    path('suggest_focus_areas/', views.suggest_focus_areas),
    path('suggest_causes/', views.suggest_causes),
    path('research_functional_needs/', views.research_functional_needs),
    path('research_emotional_needs/', views.research_emotional_needs),
    path('research_root_cause/', views.research_root_cause),
    path('brainstorm_approach/', views.brainstorm_approach),
]