from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from src.models import User

from django import forms

from django.forms.widgets import TextInput, PasswordInput, EmailInput

class registerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "",
            "password1": "",
            "password2": "",
            "email": ""
        }

        widgets = {"username": TextInput(attrs={"placeholder": "Username", "autocomplete": "off"}),
                   "password1": PasswordInput(attrs={"placeholder": "Password", "class": "passwordToggle"}),
                   "password2": PasswordInput(attrs={"placeholder": "Confirm Password", "class": "passwordToggle"}),
                   "email": EmailInput(attrs={"placeholder": "Email", "autocomplete": "off"})}

class loginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())