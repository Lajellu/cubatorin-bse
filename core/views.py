from django.shortcuts import render, redirect
from django.contrib.auth import login as loginUser, logout as logoutUser
from django.contrib import messages

from .forms import TeamLoginForm
from .decorators import team_login_required

def index(request):
    return redirect('/team/step-1')

def team_login(request):
    form_errors = None

    if request.method == 'POST':
        form = TeamLoginForm(request, request.POST)
        if form.is_valid():
            loginUser(request, form.get_user())

            username = form.cleaned_data.get('username')
            messages.success(request, 'Welcome ' + username + '!')

            return redirect('/team/step-1')
        else:
            form_errors = form.errors.get("__all__")
    else:
        form = TeamLoginForm()

    return render(request, 'core/team_login.html', {'form':form, 'form_errors':form_errors})

def team_logout(request):
    logoutUser(request)
    return redirect('/team/login')

@team_login_required
def team_step_1(request):
    return render(request, 'core/team_step_1.html')