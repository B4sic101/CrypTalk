from django.shortcuts import render, redirect
from .forms import registerForm, loginForm
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, viewsets
from src.serializers import addContact

def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:    
        return render(request, "index.html")

def dashboard(request):
    if request.user.is_authenticated:
        context = {
                "username" : request.user.username,
                "userID" : request.user.userID,
                "profileimage" : f"/uploads/profiles/user_{request.user.userID}.jpeg"
            }
        return render(request, "dashboard/dashboard.html", context=context)
    else:
        return redirect("index")

def loginView(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        form = loginForm()
        if request.method == "POST":
            form = loginForm(request, data=request.POST)
                
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    return redirect("dashboard")
                    
        context = {"loginform": form}
        return render(request, 'authentication/login.html', context=context)

def registerView(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:

        form = registerForm()
        if request.method == 'POST':
            form = registerForm(request.POST)

            if form.is_valid():
                form.save()

                return redirect("login")

        context = {"registerform": form}
        return render(request, 'authentication/register.html', context)

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")