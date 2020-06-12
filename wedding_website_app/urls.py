from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('login_now', views.login_now),
    path('register', views.register),
    path('register_now', views.register_now),
    path('logout', views.logout),
    path('add_guest', views.add_guest),
    path('see_guest', views.see_guest),
    path('erase_guest', views.erase_guest),
    path('submited', views.submited)
]
