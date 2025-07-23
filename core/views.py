from django.shortcuts import render, redirect
from django.contrib.auth import login as loginUser, logout as logoutUser
from django.contrib import messages

from core.models import MembersAndFocus
from core.models import Team
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
            # print("erroring out")
            form_errors = form.errors.get("__all__")
    else:
        form = TeamLoginForm()

    return render(request, 'core/team_login.html', {'form':form, 'form_errors':form_errors})

def team_logout(request):
    logoutUser(request)
    return redirect('/team/login')

@team_login_required
def team_step_1(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    members_and_focus = MembersAndFocus.objects.filter(team_id=team_id).first()

    if not members_and_focus: 
        members_and_focus = MembersAndFocus(team_id=team_id)
        members_and_focus.save()
    
    context = {
        "team_id": team_id,
        "member_range": range(1, 6),
        "problem_range": range(1, 6),
        "focusarea_range": range(1, 7),
        "focusarea_problem_range": range(1, 11),
        "color_list": ["", "#fffa9c", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3"],
        "members_and_focus": members_and_focus,
        "next_step_link": "/team/step-2/",
    }

    
    return render(request, "core/team_step_1.html", context)

@team_login_required
def team_step_2(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    members_and_focus = MembersAndFocus.objects.filter(team_id=team_id).first()

    if not members_and_focus: 
        members_and_focus = MembersAndFocus(team_id=team_id)
        members_and_focus.save()
    
    context = {
        "team_id": team_id,
        "member_range": range(1, 6),
        "problem_range": range(1, 6),
        "focusarea_range": range(1, 7),
        "focusarea_problem_range": range(1, 11),
        "color_list": ["", "#fffa9c", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3"],
        "members_and_focus": members_and_focus,
        "prev_step_link": "/team/step-1/",
        "next_step_link": "/team/step-3/",
    }

    
    return render(request, "core/team_step_2.html", context)