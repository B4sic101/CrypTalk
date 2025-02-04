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
        cleanedData = super().clean()
        username = cleanedData.get("username")
        email = cleanedData.get("email")
        password1 = cleanedData.get("password1")
        password2 = cleanedData.get("password2")

        if password1 != None and password2 != None:

            error = authVal.passwordValid(password1)

            if error is not None:
                self.add_error("password1", error)
        
            self.errors.pop("password2", None)

            if username is None:
                return cleanedData
            
            if User.objects.filter(username=username).exists():
                self.add_error("username", "Username taken.")
                
            if search(r"^\s|\s{2,}|\s$", username):
                self.add_error("username", "Invalid Username")

            if User.objects.filter(email=email).exists():
                self.add_error("email", "Email already exists.")

            if password1 and password2 and password1 != password2:
                self.add_error("password2", "Passwords do not match.")

            return cleanedData


class loginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

print("***forms.py loaded***")