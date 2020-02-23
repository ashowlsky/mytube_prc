from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", admin.site.urls, name='wildcard'),
    path("logout/", views.index, name='index'),
]