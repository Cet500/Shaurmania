from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User


class SignUpForm(UserCreationForm):
    name      = forms.CharField( widget = forms.TextInput( attrs = { 'class': 'form__input' } ), max_length = 60 )
    username  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}), max_length=60)
    email     = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form__input', 'autocomplete': 'off'}), max_length=254)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input', 'autocomplete': 'new-password'}), max_length=60)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input', 'autocomplete': 'new-password'}), max_length=60)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}), label='Username', max_length=128)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}), label='Password', max_length=128)
