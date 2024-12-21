from re import search
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from src.models import User

from django import forms

from django.forms.widgets import TextInput, PasswordInput, EmailInput

from src.validators import authenticationValidators as authVal 


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
    
    def clean(self):
        cleanedData = self.cleaned_data
        username = cleanedData.get("username")
        password1 = cleanedData.get("password1")
        password2 = cleanedData.get("password2")

        error = authVal.passwordValid(password1)

        if error is not None:
            self.add_error("password1", error)
    
        self.errors.pop("password2", None)

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")
        
        if search("^\s|\s{2,}|\s$", username):
            self.add_error("username", "Invalid Username")

        return cleanedData


class loginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())