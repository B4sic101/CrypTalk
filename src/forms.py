from django import forms
from django.forms import TextInput, PasswordInput, EmailInput
from .models import myUser

passwordInputWidget = {
    'password': forms.PasswordInput()
}

class RegisterForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = ['username', 'email', 'password']
        labels = {
            "username": "",
            "password": "",
            "email": ""
        }

        widgets = {"username": TextInput(attrs={"placeholder": "Username", "autocomplete": "off"}),
                   "password": PasswordInput(attrs={"placeholder": "Password", "autocomplete": "off", "class": "passwordToggle"}),
                   "email": EmailInput(attrs={"placeholder": "Email", "autocomplete": "off"})}
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = ['username', 'password']
        widgets = [passwordInputWidget]
        labels = {
            "username": "",
            "password": ""
        }
        widgets = {"username": TextInput(attrs={"placeholder": "Username", "autocomplete": "off"}),
                   "password": PasswordInput(attrs={"placeholder": "Password", "autocomplete": "off", "class": "passwordToggle"})}

class forgotPassForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = ['email']
        widgets = [passwordInputWidget]
        labels = {
            "email": ""
        }
        widgets = {"email": EmailInput(attrs={"placeholder": "Email", "autocomplete": "off"})}

