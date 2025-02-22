from re import search
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from src.models import User
from django import forms
from django.forms.widgets import TextInput, PasswordInput, EmailInput
from src.validators import authenticationValidators as authVal
from django.core.exceptions import ObjectDoesNotExist

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
    
    def clean_username(self):
        username = self.cleaned_data['username']

            
        if User.objects.filter(username=username).exists():
            self.add_error("username", "Username taken.")
        
        if search(r"^\s|\s{2,}|\s$", username):
            self.add_error("username", "Invalid Username")
        
        return username
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error("email", "Email already exists.")
        return email

    def clean(self):
        cleanedData = self.cleaned_data
        password1 = cleanedData["password1"]
        password2 = cleanedData["password2"]

        self.errors.pop("password1", None) # learnt how to do this using AI
        error = authVal.passwordValid(password1)
        if error is not None:
            self.add_error("password1", error)
    
        self.errors.pop("password2", None)

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleanedData


class loginForm(AuthenticationForm):
    username = forms.RegexField(widget=TextInput(), regex=r"^((?!(^\s|\s{2,}|\s$)).)*$")
    password = forms.RegexField(widget=PasswordInput(), regex=r"^((?!(^\s|\s|\s$)).)*$")

    def clean(self):
        try:
            cleanedData = self.cleaned_data
            username = cleanedData["username"]
            password = cleanedData["password"]
            foundUser = User.objects.get(username=username)
            if not foundUser.check_password(password):
                raise ValueError("password no match")
        except (ValueError, KeyError, User.DoesNotExist):
            self.errors.pop("password", None)
            self.add_error("password", "Invalid credentials")

        return cleanedData

print("***forms.py loaded***")