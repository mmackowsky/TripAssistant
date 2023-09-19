from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignupForm(UserCreationForm):
    username = forms.CharField(label="Username", min_length=5, max_length=150)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="first_name", min_length=3, max_length=25, required=False
    )
    last_name = forms.CharField(
        label="last_name", min_length=2, max_length=50, required=False
    )
    username = forms.CharField(label="username", min_length=5, max_length=150)
    email = forms.EmailField(label="email")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
