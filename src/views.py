import re
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

from .forms import registerForm, loginForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout 

from src.models import User

def index(request):
    return render(request, "index.html")

def dashboard(request):
    return render(request, "dashboard.html")

def loginView(request):
    form = loginForm()
    if request.method == "POST":
        form = loginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("dashboard")
            
    context = {"loginform": form}
    return render(request, 'authentication/login.html', context=context)

def registerView(request):
    form = registerForm()
    if request.method == 'POST':
        form = registerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    context = {"registerform": form}
    return render(request, 'authentication/register.html', context=context)