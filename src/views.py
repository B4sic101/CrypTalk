from django.shortcuts import render, redirect
from .forms import registerForm, loginForm
from django.contrib.auth import authenticate, login, logout
from api.models import friendRequest 
from src.models import User
from django.core import serializers

def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:    
        return render(request, "index.html")

def dashboard(request):
    if request.user.is_authenticated:
        userFRs = friendRequest.objects.filter(receiver=request.user.userID)
        updatedUserFRs = userFRs.values()

        for fRequest in updatedUserFRs:
            senderID = fRequest["sender"]
            
            userQuery = User.objects.filter(userID=senderID).values("username")
            fRequest['senderUsername'] = userQuery[0]["username"]

            fRequest['senderProfile'] = f'/uploads/profiles/user_{senderID}.jpeg'
        
        userData = {
                "username" : request.user.username,
                "userID" : request.user.userID,
                "profileimage" : f"/uploads/profiles/user_{request.user.userID}.jpeg",
                "friendRequests" : updatedUserFRs,
        }

        return render(request, "dashboard/dashboard.html", context=userData)
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