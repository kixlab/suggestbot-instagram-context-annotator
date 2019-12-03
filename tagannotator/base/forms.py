from django import forms
from django.contrib.auth.models import User
from .models import *
from django.db import models 


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
