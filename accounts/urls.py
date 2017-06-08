# coding=utf-8

from django.conf.urls import url
from .views import index, register_view, login_view, logout_view


urlpatterns = [
    url(r'^$', index),
    url(r'^register', register_view),
    url(r'^login', login_view),
    url(r'^logout', logout_view),
]
