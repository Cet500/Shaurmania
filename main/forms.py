from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

ab

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required field. Enter active Email.')