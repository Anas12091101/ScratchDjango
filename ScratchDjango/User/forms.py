from django import forms

from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ["name", "email", "password", "otp_enabled"]


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

