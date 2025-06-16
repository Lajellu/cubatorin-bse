from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .models import Team

def team_login_required(view_func):
    def wrapper_func (request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('/team/login')

        if not Team.objects.filter(user_id=request.user.id).exists():
            return redirect('/team/login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper_func
