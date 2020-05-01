from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import AuthenticationForm, SignUpForm, AccountForm
from .models import Profile


def authentication(request):
    error = False
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = authenticate(username=username, password=password)
                login(request, user)
            except Exception:
                error = True
        else:
            error = True
    else:
        form = AuthenticationForm()

    return render(request, 'authentication.html', {
        'form': form,
        'error': error,
        'header': True
    })


def view_logout(request):
    logout(request)
    return redirect('user:authentication')


def sign_up(request):
    error = False

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(email, email, password)
            if request.FILES:
                profile = Profile(user=user, avatar=request.FILES['avatar'])
            else:
                profile = Profile(user=user)
            profile.save()
            return redirect('user:authentication')
        else:
            error = True
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {
        'form': form,
        'error': error,
        'header': True
    })


def account(request):
    error = False

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)
        form = AccountForm(instance=user)
    else:
        profile = {}
        form = {}
        error = True

    return render(request, 'account.html', {
        'profile': profile,
        'form': form,
        'error': error
    })
