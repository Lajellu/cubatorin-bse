from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Advisee

class AdviseeRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class AdviseeLoginForm(AuthenticationForm):
    class Meta:
        model = User
    
    def confirm_login_allowed(self, user):
        # ensure user is active
        if not user.is_active:
            raise ValidationError("This account is inactive.")
            
        # ensure user is an advisee
        if not Advisee.objects.filter(user_id=user.id).exists():
            raise ValidationError("Sorry, you are not an advisee.")