from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Advisor

class AdvisorRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(AdvisorRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'First Name',
            'autofocus': True,
            'required': True
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Last Name',
            'required': True
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Username'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Email address',
            'required': True
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Repeat Password'
        })

class AdvisorLoginForm(AuthenticationForm):
    class Meta:
        model = User
    
    def __init__(self, *args, **kwargs):
        super(AdvisorLoginForm, self).__init__(*args, **kwargs)

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
            
        # ensure user is an Advisor
        if not Advisor.objects.filter(user_id=user.id).exists():
            raise ValidationError("Sorry, you are not an advisor.")