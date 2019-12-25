from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'description', 'image']
