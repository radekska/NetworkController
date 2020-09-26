"""WebAppLAN_MonitorDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from config_app.views import config_detail_view, config_create_view
from login_app.views import login_view, logout_view
from registration_app.views import registration_view
from dashboard_app.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration_view, name='registration'),

    path('dashboard/', dashboard_view, name='dashboard'),
    path('configview/', config_detail_view, name='configview'),
    path('configcreate/', config_create_view, name='configcreate'),

    # Built in path to login view
    # path('', include('django.contrib.auth.urls')),

]

urlpatterns += staticfiles_urlpatterns()
