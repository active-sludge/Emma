from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from emmaApp.utils import android_management_api, policy_manager


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
                android_management_api.authenticate_google_user()
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
    if android_management_api.androidmanagement is None:
        android_management_api.authenticate_google_user()

    fully_managed_policy_option_list = policy_manager.fully_managed_policy_option_list
    byod_policy_option_list = policy_manager.byod_policy_option_list
    # byod_application_available_install_package_name_list = policy_manager.byod_application_available_install_package_name_list
    # byod_application_block_install_package_name_list = policy_manager.byod_application_block_install_package_name_list

    enterprise_name = android_management_api.get_enterprise_name()

    if request.method == 'GET':
        context = {
            'enterprise_name': enterprise_name,
            'fully_managed_policy_option_list': fully_managed_policy_option_list,
            'byod_policy_option_list': byod_policy_option_list,
        }
        return render(request, 'emma/policies.html', context)
    else:
        if 'create_policy' in request.POST:
            policy_dict = {}
            policy_options = request.POST.getlist('policy_options')
            byod_policy_options = request.POST.getlist('byod_policy_options')
            policy_name = request.POST.get('policy_name')

            for policy_option in policy_options:
                policy_dict[policy_option] = True

            for byod_policy_option in byod_policy_options:
                byod_policy = byod_policy_option_list[int(byod_policy_option)]
                policy_options.append(byod_policy['policy_key'])
                policy_dict[byod_policy['policy_key']] = byod_policy['policy_json']

            policy_full_name = android_management_api.create_policy(policy_name, policy_dict)

            context = {
                'enterprise_name': enterprise_name,
                'fully_managed_policy_option_list': fully_managed_policy_option_list,
                'byod_policy_option_list': byod_policy_option_list,
                'policy_name': policy_full_name,
                'policy_options': policy_options
            }
            return render(request, 'emma/policies.html', context)
        elif 'enroll_device' in request.POST:
            enterprise_name = android_management_api.get_enterprise_name()
            policy_full_name = request.POST.get('policy_name')
            
            qrcode_url = android_management_api.enroll_device(enterprise_name, policy_full_name)
            context = {
                'enterprise_name': enterprise_name,
                'fully_managed_policy_option_list': fully_managed_policy_option_list,
                'byod_policy_option_list': byod_policy_option_list,
                'policy_name': policy_full_name,
                'qrcode_url': qrcode_url,
            }
            return render(request, 'emma/policies.html', context)


def devices(request):
    if android_management_api.androidmanagement is None:
        android_management_api.authenticate_google_user()

    if request.method == 'POST':
        if 'delete_device' in request.POST:
            device_name = request.POST.get('device_name')
            android_management_api.delete_device(device_name)
            return redirect('devices')
        elif 'lock_device' in request.POST:
            device_name = request.POST.get('device_name')
            android_management_api.lock_device(device_name)
            return redirect('devices')
        elif 'restart_device' in request.POST:
            device_name = request.POST.get('device_name')
            android_management_api.restart_device(device_name)
            return redirect('devices')
        else:
            pass
    else:
        devices = android_management_api.get_devices()

        context = {
            'devices': devices
        }

        return render(request, 'emma/devices.html', context)
