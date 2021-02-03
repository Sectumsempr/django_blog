from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    about = forms.CharField(widget=forms.Textarea, required=False, help_text='О себе')
    file_field = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'about', 'password1', 'password2')


class EditRegisterForm(UserChangeForm):
    password = None
    about = forms.CharField(widget=forms.Textarea, required=False, help_text='О себе')
    file_field = forms.FileField(required=False, help_text='Фотография профиля')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'about')
