from django import forms

from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["name", "email", "password", "otp_enabled"]


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["email", "password"]


class ResetForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("password", "confirm_password")


class ResetEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
