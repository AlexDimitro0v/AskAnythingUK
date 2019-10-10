from django import forms
from django.contrib.auth.models import User
from .models import FeedbackRequest
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class NewFeedbackRequestForm(forms.Form):
    title = forms.CharField()
    maintext = forms.CharField()

    class Meta:
        model = FeedbackRequest
        fields = ['title','maintext']
