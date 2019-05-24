from django import forms
from django.contrib.auth.models import User

from .models import SignLanguage, Huruf

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class SignLanguageForm(forms.ModelForm):
   
    class Meta:
        model = SignLanguage
        fields = ['name', 'website', 'logo']

class HurufForm(forms.ModelForm):

    class Meta:
        model = Huruf
        fields = ['huruf','cover']