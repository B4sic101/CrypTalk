from django.shortcuts import render, redirect
from .forms import registerForm, loginForm
from django.contrib.auth import authenticate, login, logout
from api.models import friendRequest
from api.models import chat as modelChat
from src.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:    
        return render(request, "index.html")

@login_required
def dashboard(request):
    thisUserID = request.user.userID
    userFRs = friendRequest.objects.filter(receiver=thisUserID)
    updatedUserFRs = userFRs.values()

    for fRequest in updatedUserFRs:
        senderID = fRequest["sender"]
        
        userQuery = User.objects.filter(userID=senderID).values("username")
        fRequest['senderUsername'] = userQuery[0]["username"]
    
    userChats = modelChat.objects.filter(Q(sender=thisUserID) | Q(receiver=thisUserID)).values()

    for chat in userChats:
        if chat["sender"] == thisUserID:
            chat['username'] = User.objects.get(userID=chat["receiver"]).username
            chat['sender'] = chat["receiver"]
        else:
            chat['username'] = User.objects.get(userID=chat["sender"]).username

    # Latest message must change to You if there is a message and if the message was sent by sender or receiver, must cut the part out and change it adaquetly.
    
    userData = {
            "username" : request.user.username,
            "userID" : thisUserID,
            "profileimage" : f"/uploads/profiles/user_{thisUserID}.jpeg",
            "friendRequests" : updatedUserFRs,
            "chats": userChats,
    }

    return render(request, "dashboard/dashboard.html", context=userData)


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

@login_required
def logout_user(request):
    logout(request)
    return redirect("index")