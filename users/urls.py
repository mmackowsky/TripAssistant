from django.contrib import admin
from django.urls import path
from .views import signup, activate, login_request, logout_request


urlpatterns = [
    path("signup", signup, name="signup"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path("login", login_request, name="login")
]
