from django import forms
from django.contrib.auth.models import User
from .models import FeedbackRequest
from .models import Feedbacker
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NewFeedbackRequestForm(forms.Form):
    title = forms.CharField()
    maintext = forms.CharField()
    reward = forms.IntegerField()

    class Meta:
        model = FeedbackRequest
        fields = ['title', 'maintext', 'reward']


class FedbackerProfileForm(forms.Form):
    description = forms.CharField()

    class Meta:
        model = Feedbacker
        fields = ['description']
