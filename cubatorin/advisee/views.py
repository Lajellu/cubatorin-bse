from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as loginUser, logout as logoutUser
from django.contrib import messages
from django.db import transaction

from .forms import AdviseeRegistrationForm
from .forms import AdviseeLoginForm
from .models import Advisee
from .decorators import advisee_login_required

@advisee_login_required
def dashboard(request):
    return render(request, 'advisee/dashboard.html')

def index(request):
    return render(request, 'advisee/index.html')

def logout(request):
    logoutUser(request)
    return redirect('/advisee')

def login(request):
    form_errors = None;

    if request.method == 'POST':
        form = AdviseeLoginForm(request, request.POST)
        if form.is_valid():
            loginUser(request, form.get_user())

            username = form.cleaned_data.get('username')
            messages.success(request, 'Welcome ' + username + '!')

            return redirect('/advisee/dashboard')
        else:
            form_errors = form.errors.get("__all__")
    else:
        form = AdviseeLoginForm()

    return render(request, 'advisee/login.html', {'form':form, 'form_errors':form_errors})

def register(request):
    if request.method == 'POST':
        form = AdviseeRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
            
                    advisee = Advisee.objects.create(user=user)
            except Exception as e:
                print(f"Exception: {e}")
            else:
                # username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user.username + '. You can now login!')

            return redirect('/advisee/login/')
    else:
        form = AdviseeRegistrationForm()
    
    return render(request, 'advisee/register.html', {'form':form})
