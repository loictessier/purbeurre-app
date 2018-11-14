from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import AuthenticationForm, SignUpForm

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

def sign_up(request):
    # TODO
    pass
