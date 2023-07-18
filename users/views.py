from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .forms import SignupForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpRequest


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_activate = False
            user.save()
            to_email = form.cleaned_data.get('email')
            send_email(request, user, to_email)
            return HttpResponse('Please confirm your email address to complete registration')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def send_email(request: HttpRequest, user: User, to_email: str) -> None:
    current_site = get_current_site(request)
    mail_subject = 'Activation link has been sent to your email id'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def get_user_by_uid(uid64):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        return User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


def activate_user(user, token) -> bool:
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    return False


def activate(request, uid64, token):
    user = get_user_by_uid(uid64)
    if activate_user(user, token):
        return HttpResponse('Thank you for email confirmation. Now you can login your account')
    else:
        return HttpResponse('Activation link is invalid')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Hello {username}!')
                return redirect('users/login.html')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request=request, template_name='users/login.html', context={'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'Successfully logout.')
    return redirect('users/login.html')


# def profile(request):
#
