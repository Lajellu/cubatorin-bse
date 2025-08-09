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
    path('brainstorm_test_method/', views.brainstorm_test_method),
    path('suggest_customer_profiles/', views.suggest_customer_profiles),
    path('suggest_benefits_costs/', views.suggest_benefits_costs),
    
    
]