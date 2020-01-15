from django import forms
from .models import FeedbackRequest
# from .models import Feedbacker
from .models import FeedbackerComments
from .models import Rating


class NewFeedbackRequestForm(forms.Form):
    title = forms.CharField()
    maintext = forms.CharField()
    reward = forms.IntegerField()
    timelimit = forms.IntegerField()

    class Meta:
        model = FeedbackRequest
        fields = ['title', 'maintext', 'reward', 'timelimit']


# class FedbackerProfileForm(forms.Form):
#    description = forms.CharField()
#
#     class Meta:
#         model = Feedbacker
#         fields = ['description']


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
        fields = ["quality","speed","communication","review"]
