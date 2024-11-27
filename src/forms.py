from django import forms
from .models import myUser

passwordInputWidget = {
    'password': forms.PasswordInput()
}

class RegisterForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = ['username', 'email', 'password']
        widgets = [passwordInputWidget]

class LoginForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = ['username', 'password']
        widgets = [passwordInputWidget]

