import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from emmaApp.utils import android_management_api


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
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'emma/login.html', {'form': AuthenticationForm(),
                                                       'error': 'Username and password did not match.'}
                          )
        else:
            login(request, user)
            android_management_api.authenticate_google_user()
            return redirect('home')


@login_required
def log_out_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def enterprise(request):
    if request.method == 'GET':
        return render(request, 'emma/enterprise.html')
    else:
        if 'create_enterprise' in request.POST:
            url = android_management_api.create_enterprise()
            context = {
                'url': url,
            }
            return render(request, 'emma/enterprise.html', context)
        elif 'enter_token' in request.POST:
            token = request.POST['enterprise_token']
            print(token)
            enterprise_name = android_management_api.enter_enterprise_token(token)
            context = {
                'enterprise_name': enterprise_name,
            }
            return render(request, 'emma/enterprise.html', context)


@login_required
def policies(request):
    if request.method == 'GET':
        return render(request, 'emma/policies.html')
    else:
        if 'create_policy' in request.POST:
            policy_name = android_management_api.create_policy()
            context = {
                'policy_name': policy_name,
            }
            return render(request, 'emma/policies.html', context)
        elif 'enroll_device' in request.POST:
            policy_name = android_management_api.get_policy_name()
            qrcode_url = android_management_api.enroll_device(policy_name)
            context = {
                'qrcode_url': qrcode_url,
            }
            return render(request, 'emma/policies.html', context)


def devices(request):
    if android_management_api.androidmanagement is None:
        android_management_api.authenticate_google_user()

    device_list_json = android_management_api.get_devices()
    print(device_list_json)
    context = {
        'devices': device_list_json
    }
    return render(request, 'emma/devices.html', context)
