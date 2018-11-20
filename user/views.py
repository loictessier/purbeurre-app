from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import AuthenticationForm, SignUpForm
from .models import Profile


def authentication(request):
    error = False
    
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = AuthenticationForm()  

    return render(request, 'authentication.html', {
        'form': form,
        'error': error
    })


def view_logout(request):
    logout(request)
    return redirect('/')


def sign_up(request):
    error = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(email, email, password)
            profile = Profile(user=user)
            profile.save()
            return redirect('/')
        else:
            error = True
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {
        'form': form,
        'error': error
    })
