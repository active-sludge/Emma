"""EmmaProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from emmaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.sign_up_user, name='signupuser'),
    path('logout/', views.log_out_user, name='logoutuser'),
    path('login/', views.log_in_user, name='loginuser'),

    path('', views.home, name='home'),
    path('enterprise', views.enterprise, name='enterprise'),
    path('enterprise/create', views.create_enterprise, name='create_enterprise'),

    path('policies', views.policies, name='policies'),
]
