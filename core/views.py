from django.shortcuts import render, redirect
from django.contrib.auth import login as loginUser, logout as logoutUser
from django.contrib import messages

from .forms import TeamLoginForm
from .decorators import team_login_required

from core.models import Team, MembersAndFocus, OpportunityDiscovery, UserNeed, RootCause, HowMightWe, SolutionIdeation, SolutionSelection, SolutionValidation, FirstCustomer, Pitch

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
    opportunity_discovery = OpportunityDiscovery.objects.filter(team_id=team_id).first()

    if not opportunity_discovery: 
        opportunity_discovery = OpportunityDiscovery(team_id=team_id)
        opportunity_discovery.save()
    
    context = {
        "team_id": team_id,
        "diverge_table_range": range(1, 7),
        "difficulty_range": range(1, 6),
        "impact_range": range(1, 6),
        "color_list": ["", "#fffa9c", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "opportunity_discovery": opportunity_discovery,
        "prev_step_link": "/team/step-1/",
        "next_step_link": "/team/step-3/",
    }

    
    return render(request, "core/team_step_2.html", context)

@team_login_required
def team_step_3(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    user_need = UserNeed.objects.filter(team_id=team_id).first()

    if not user_need: 
        user_need = UserNeed(team_id=team_id)
        user_need.save()
    
    context = {
        "team_id": team_id,
        "diverge_table_range": range(1, 5),
        "color_list": ["", "#fffa9c", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "user_need": user_need,
        "prev_step_link": "/team/step-2/",
        "next_step_link": "/team/step-4/",
    }

    
    return render(request, "core/team_step_3.html", context)

@team_login_required
def team_step_4(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    root_cause = RootCause.objects.filter(team_id=team_id).first()

    if not root_cause: 
        root_cause = RootCause(team_id=team_id)
        root_cause.save()
    
    context = {
        "team_id": team_id,
        "diverge_table_range": range(1, 6),
        "color_list": ["", "#fffa9c", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "root_cause": root_cause,
        "prev_step_link": "/team/step-3/",
        "next_step_link": "/team/step-5/",
    }

    
    return render(request, "core/team_step_4.html", context)

@team_login_required
def team_step_5(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    how_might_we = HowMightWe.objects.filter(team_id=team_id).first()
    root_cause = RootCause.objects.filter(team_id=team_id).first()

    if not how_might_we: 
        how_might_we = HowMightWe(team_id=team_id)
        how_might_we.save()
    
    context = {
        "team_id": team_id,
        "diverge_table_range": range(1, 6),
        "top_hmw_range": range(1,4),
        "color_list": ["", "#fffa9c", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "how_might_we": how_might_we,
        "root_cause": root_cause,
        "prev_step_link": "/team/step-4/",
        "next_step_link": "/team/step-6/",
    }

    
    return render(request, "core/team_step_5.html", context)

@team_login_required
def team_step_6(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    solution_ideation = SolutionIdeation.objects.filter(team_id=team_id).first()

    if not solution_ideation: 
        solution_ideation = SolutionIdeation(team_id=team_id)
        solution_ideation.save()
    
    context = {
        "team_id": team_id,
        "diverge_range": range(1, 8),
        "solution_group_range": range(1,5),
        "approach_group_range": range(1,4),
        "approach_range": range(1,6),
        "color_list": ["", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "solution_ideation": solution_ideation,
        "prev_step_link": "/team/step-5/",
        "next_step_link": "/team/step-7/",
    }

    
    return render(request, "core/team_step_6.html", context)

@team_login_required
def team_step_7(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    solution_ideation = SolutionIdeation.objects.filter(team_id=team_id).first()
    solution_selection = SolutionSelection.objects.filter(team_id=team_id).first()

    if not solution_ideation: 
        solution_ideation = SolutionIdeation(team_id=team_id)
        solution_ideation.save()
    
    context = {
        "team_id": team_id,
        "solution_group_range": range(1,5),
        "approach_group_range": range(1,4),
        "color_list": ["", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "solution_ideation": solution_ideation,
        "solution_selection": solution_selection,
        "prev_step_link": "/team/step-6/",
        "next_step_link": "/team/step-8/",
    }

    
    return render(request, "core/team_step_7.html", context)

@team_login_required
def team_step_8(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    solution_validation = SolutionValidation.objects.filter(team_id=team_id).first()

    if not solution_validation: 
        solution_validation = SolutionValidation(team_id=team_id)
        solution_validation.save()
    
    context = {
        "team_id": team_id,
        "feature_range": range(1,5),
        "fields_range": range(1,9),
        "color_list": ["", "#b6e560", "#ffd4f3", "#b2d0fd", "#b9adfb"],
        "solution_validation": solution_validation,
        "fields": [
            "",
            "desc",
            "func_need",
            "test_method",
            "test_method_alt",
            "emot_need",
            "proto_test",
            "who_test",
            "where_test",
            "proto_test_desc",
            "proto_test_question",
            "proto_test_satisfaction",
        ],
        "field_descs": [
            "",
            "Description of feature", 
            "Explain how it meets user functional need",
            "How could you test this?",
            "Alternate way to test this?",
            "Explain how it meets user emotinoal need",
            "Design your prototype test",
            "Who will you test it with? (e.g. Family, friends, BSE participants, your professor, etc.)",
            "Who will test it and where will they test it?",
        ],
        "row_backgrounds": [
            "",
            "#fdf545",
            "#808080",
            "#f5f5f5",
            "#f5f5f5",
            "#f5f5f5",
            "#808080",
            "#808080",
            "#f5f5f5",
            "#f5f5f5",
        ],
        "feature_postit_colors": [
            "",
            "#b4e660",
            "#ffd1f1",
            "#b3d1fe",
            "#bfb4fb",
        ],
        "prev_step_link": "/team/step-7/",
        "next_step_link": "/team/step-9/",
    }

    
    return render(request, "core/team_step_8.html", context)

@team_login_required
def team_step_9(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    first_customer = FirstCustomer.objects.filter(team_id=team_id).first()

    if not first_customer: 
        first_customer = FirstCustomer(team_id=team_id)
        first_customer.save()
    
    context = {
        "team_id": team_id,
        "customer_range": range(1,5),
        "color_list": ["", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "first_customer": first_customer,
        "prev_step_link": "/team/step-8/",
        "next_step_link": "/team/step-10/",
    }

    
    return render(request, "core/team_step_9.html", context)

@team_login_required
def team_step_10(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    pitch = Pitch.objects.filter(team_id=team_id).first()

    if not pitch: 
        pitch = Pitch(team_id=team_id)
        pitch.save()
    
    context = {
        "team_id": team_id,
        "row_range": range(1, 7),
        "postit_range": range(1,5),
        "row_criteria": [
            "",
            "Evidence of the problem",
            "Evidence of novelty and inventiveness (patentability and other IP)",
            "Evidence each solution meets users’ functional and emotional needs.",
            "Evidence that solution is feasible and implementable.",
            "Evidence that solution is viable and sustainable.",
            "Solution represents a creative approach to solving problem.",
            "First Customer",
        ],
        "row_expectation": [
            "",
            "Clear evidence of problem, its importance & who is affected by it.",
            "Obvious evidence of a technical advancement as compared to the existing knowledge",
            "Good evidence / explanation of how solution meets both emotional & functional needs of user.",
            "Detailed evidence that the solution proposed will work and can be implemented.",
            "Strong and compelling evidence that solution is viable & sustainable.",
            "Extremely creative solution - a radically new approach to solving problem.",
            "Strong evidence that first customer wants and is able to adopt solution in short term.",
        ],
        "row_field": [
            "",
            "evidence_problem",
            "evidence_novelty",
            "evidence_feasible",
            "evidence_viable",
            "creative_approach",
            "first_customer",
        ],
        "color_list": ["", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "pitch": pitch,
        "prev_step_link": "/team/step-9/",
        "next_step_link": "/team/step-11/",
    }

    
    return render(request, "core/team_step_10.html", context)

@team_login_required
def team_step_11(request):
    user_id = request.user.id
    team_id = Team.objects.filter(user_id=user_id).first().id
    first_customer = FirstCustomer.objects.filter(team_id=team_id).first()

    if not first_customer: 
        first_customer = FirstCustomer(team_id=team_id)
        first_customer.save()
    
    context = {
        "team_id": team_id,
        "customer_range": range(1,5),
        "color_list": ["", "#fbeb7d", "#daf1a9", "#9ce7ff", "#f9d6f3", "#b2b7e1"],
        "first_customer": first_customer,
        "prev_step_link": "/team/step-10/",
    }

    
    return render(request, "core/team_step_11.html", context)