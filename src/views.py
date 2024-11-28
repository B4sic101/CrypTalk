import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from src.forms import LoginForm, RegisterForm, forgotPassForm
from src.models import myUser


def index(request):
    return render(request, 'index.html')
def dashboard(request):
    return HttpResponse("This is the user dashboard")
def login(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        if myUser.objects.filter(username=request.POST['username']).exists():
            error = "Username is taken."
            return render(request, 'register.html', {'form': form, 'error': error})
        if myUser.objects.filter(email=request.POST['email']).exists():
            error = "An account with this email already exists."
            return render(request, 'register.html', {'form': form, 'error': error})
        if re.search("^\s|\s{2,}|\s$", request.POST["username"]):
            error = "Username must have spaces in appropriate places"
            return render(request, 'register.html', {'form': form, 'error': error})
        form = RegisterForm(request.POST)
        new_user = form.save(commit=False)
        new_user.save()
        return HttpResponseRedirect("/login/")
    return render(request, 'register.html', {'form': form})

def forgotPassword(request):
    form = forgotPassForm()
    if request.method == 'POST':
        if myUser.objects.filter(email=request.POST['email']).exists():
            # The email exists, send the reset link and return page to indicate if email exists then sent
            d = d
    return render(request, 'forgotPassword.html', {'form': form})

