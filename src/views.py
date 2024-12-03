import re
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from src.forms import LoginForm, RegisterForm, forgotPassForm
from src.models import myUser

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def index(request):
    return render(request, 'index/index.html')
def dashboard(request):
    return HttpResponse("This is the user dashboard")
def login(request):
    form = LoginForm()
    return render(request, 'authentication/login/login.html', {'form': form})
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        if myUser.objects.filter(username=request.POST['username']).exists():
            error = "Username is taken."
            return render(request, 'authentication/register/register.html', {'form': form, 'error': error})
        if myUser.objects.filter(email=request.POST["email"]).exists():
            error = "An account with this email already exists."
            return render(request, 'authentication/register/register.html', {'form': form, 'error': error})
        if re.search("^\s|\s{2,}|\s$", request.POST["username"]):
            error = "Username must have spaces in appropriate places"
            return render(request, 'authentication/register/register.html', {'form': form, 'error': error})
        if not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$", request.POST["password"]):
            error = "Password invalid, for valid: 8 characters minimum, one lowercase & uppercase letter, one number, and one special character."
            return render(request, 'authentication/register/register.html', {'form': form, 'error': error})
        form = RegisterForm(request.POST)
        new_user = form.save(commit=False)
        new_user.save()
        return HttpResponseRedirect("/login/")
    return render(request, 'authentication/register/register.html', {'form': form})