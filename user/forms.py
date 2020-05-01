from django import forms
from django.contrib.auth.models import User


class AuthenticationForm(forms.Form):
    username = forms.EmailField(label="Adresse email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    avatar = forms.FileField(required=False)
    email = forms.EmailField(label="Adresse email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Le mot de passe et la confirmation du mot de passe ne correspondent pas"
            )


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'disabled': True}),
        }
