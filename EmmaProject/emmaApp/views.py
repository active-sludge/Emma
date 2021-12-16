from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    return render(request, 'emma/home.html')


def sign_up_user(request):
    if request.method == "GET":
        return render(request, 'emma/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'emma/signup.html',
                              {'form': UserCreationForm(),
                               'error': 'That user name has already has been taken. Please choose a new username.'})
        else:
            return render(request, 'emma/signup.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def log_in_user(request):
    if request.method == "GET":
        return render(request, 'emma/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'emma/login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('home')


@login_required
def log_out_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')