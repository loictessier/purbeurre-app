from django import forms


class AuthenticationForm(forms.Form):
    username = forms.CharField(label="Adresse email", max_length=50)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    email = forms.CharField(label="Adresse email", max_length=50)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)