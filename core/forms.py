from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Team

class TeamLoginForm(AuthenticationForm):
    class Meta:
        model = Team
    
    def __init__(self, *args, **kwargs):
        super(TeamLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Password'
        })
    
    def confirm_login_allowed(self, user):
        # ensure user is active
        if not user.is_active:
            raise ValidationError("This account is inactive.")
            
        # ensure user is an advisee
        if not Team.objects.filter(user_id=user.id).exists():
            raise ValidationError("Sorry, you are not a team.")