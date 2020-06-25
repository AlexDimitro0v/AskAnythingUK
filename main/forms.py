from django import forms
from .models import FeedbackRequest
from .models import FeedbackerComments
from .models import Rating
from .models import FeedbackerCandidate
from .models import Message


class NewFeedbackRequestForm(forms.Form):
    area = forms.IntegerField()
    title = forms.CharField()
    maintext = forms.CharField()
    reward = forms.IntegerField(min_value=5)
    timelimit = forms.IntegerField(min_value=1)

    class Meta:
        model = FeedbackRequest
        fields = ['area', 'title', 'maintext', 'reward', 'timelimit']


class FeedbackerCommentsForm(forms.Form):
    comments = forms.CharField(required=False)

    class Meta:
        model = FeedbackerComments
        fields = ['comments']


class FeedbackerRatingForm(forms.Form):
    overall = forms.IntegerField(min_value=0,max_value=5)
    quality = forms.IntegerField(min_value=0,max_value=5)
    speed = forms.IntegerField(min_value=0,max_value=5)
    communication = forms.IntegerField(min_value=0,max_value=5)
    review = forms.CharField(required=False)

    class Meta:
        model = Rating
        fields = ["overall", "quality", "speed", "communication", "review"]


class ApplicationForm(forms.Form):
    application = forms.CharField()
    proposed_reward = forms.IntegerField(min_value=5)

    class Meta:
        model = FeedbackerCandidate
        fields = ["application","proposed_reward"]


class MessageForm(forms.Form):
    message = forms.CharField()

    class Meta:
        model = Message
        fields = ["message"]
