import logging
import os
from tempfile import TemporaryDirectory
from typing import Union

import boto3
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import FormView, TemplateView

from .forms import ProfileUpdateForm, SignupForm, UserUpdateForm
from .tokens import account_activation_token


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        to_email = form.cleaned_data.get("email")
        self.send_email(user, to_email)
        messages.info(
            self.request, "Please confirm your email address to complete registration"
        )
        return redirect("login")

    def form_invalid(self, form):
        self.error_messages(form)
        logging.error("Form is not valid.")
        return super().form_invalid(form)

    def send_email(self, user, to_email):
        current_site = get_current_site(self.request)
        mail_subject = "Activation link has been sent to your email id"
        message = render_to_string(
            "users/acc_active_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        logging.debug("Email sent in activation case.")

    def error_messages(self, form):
        error_messages = []

        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{error}")

        for error_message in error_messages:
            messages.error(self.request, error_message)


class ActivateView(View):
    def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
        user = ActivateView.get_user_by_uid(uidb64)
        if self._activate_user(user, token):
            messages.success(
                request,
                "Thank you for email confirmation. Now you can log in to your account",
            )
            return redirect("login")
        messages.warning(request, "Activation link is invalid")
        return redirect("signup")

    @staticmethod
    def get_user_by_uid(uidb64: str) -> Union[User, None]:
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            logging.error(f"Issue in get_user_by_uid: {e}")
            return None

    def _activate_user(self, user: User, token: str) -> bool:
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return True
        logging.warning("User is not activate")
        return False


class ProfileView(View, LoginRequiredMixin):
    def get(self, request: HttpRequest) -> HttpResponse:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(
            request,
            "users/profile.html",
            {"user_form": user_form, "profile_form": profile_form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            profile_image = profile_form.cleaned_data.get("image")

            # Temporary directory
            self._save_to_s3(profile_image)

            # Save data
            user_form.save()
            profile_form.save()

            messages.success(request, "Successful update")
            return redirect("profile")
        logging.error("Form is not valid")
        return render(
            request,
            "users/profile.html",
            {"user_form": user_form, "profile_form": profile_form},
        )

    def _save_to_s3(self, profile_image: InMemoryUploadedFile) -> None:
        logging.debug("Saving profile image to S3")
        with TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, profile_image.name)

            # Saving InMemoryUploadedFile to temp_file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(profile_image.read())

            # Sending to S3
            s3 = boto3.client("s3")
            s3.upload_file(
                temp_file_path,
                settings.AWS_STORAGE_BUCKET_NAME,
                profile_image.name,
            )


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = AuthenticationForm()
        return render(
            request=request,
            template_name="users/login.html",
            context={"login_form": form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            next_url = self.request.session.get("next")
            if user is not None:
                login(request, user)
                messages.info(request, f"Hello {username}!")
                if next_url:
                    del self.request.session["next"]
                    return redirect(next_url)
                else:
                    return redirect(reverse("home"))
        messages.error(request, "Invalid username or password.")
        return render(
            request=request,
            template_name="users/login.html",
            context={"login_form": form},
        )


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        messages.info(request, "Successfully logout.")
        return redirect("login")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("home")


class SocialNotAvailableView(TemplateView):
    template_name = "users/social_login_not_available.html"
