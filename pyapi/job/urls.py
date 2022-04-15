from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^job/?$', views.job),
    re_path(r'^result/?$', views.result),
]