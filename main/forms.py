from django import forms
from .models import FeedbackRequest
from .models import FeedbackerComments
from .models import Rating
from .models import FeedbackerCandidate


class NewFeedbackRequestForm(forms.Form):
    area = forms.IntegerField()
    title = forms.CharField()
    maintext = forms.CharField()
    reward = forms.IntegerField()
    timelimit = forms.IntegerField()

    class Meta:
        model = FeedbackRequest
        fields = ['area', 'title', 'maintext', 'reward', 'timelimit']


class FeedbackerCommentsForm(forms.Form):
    comments = forms.CharField(required=False)

    class Meta:
        model = FeedbackerComments
        fields = ['comments']


class FeedbackerRatingForm(forms.Form):
    quality = forms.IntegerField()
    speed = forms.IntegerField()
    communication = forms.IntegerField()
    review = forms.CharField()

    class Meta:
        model = Rating
        fields = ["quality", "speed", "communication", "review"]

class ApplicationForm(forms.Form):
    application = forms.CharField()

    class Meta:
        model = FeedbackerCandidate
        fields = ["application"]
