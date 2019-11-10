from django import forms
from .models import FeedbackRequest
from .models import Feedbacker
from .models import FeedbackerComments


class NewFeedbackRequestForm(forms.Form):
    title = forms.CharField()
    maintext = forms.CharField()
    reward = forms.IntegerField()
    timelimit = forms.IntegerField()

    class Meta:
        model = FeedbackRequest
        fields = ['title', 'maintext', 'reward','timelimit']


class FedbackerProfileForm(forms.Form):
    description = forms.CharField()

    class Meta:
        model = Feedbacker
        fields = ['description']

class FeedbackerCommentsForm(forms.Form):
    comments = forms.CharField()

    class Meta:
        model = FeedbackerComments
        fields = ['comments']
