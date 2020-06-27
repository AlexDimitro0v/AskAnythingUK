from .models import FeedbackRequest, FeedbackerCandidate
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from users.models import UserProfile


def get_time_delta(time_0, time_1):
        delta = time_1 - time_0
        if delta.days > 1:
            time_delta = str(delta.days) + " days"
        elif delta.days == 1:
            time_delta = str(delta.days) + " day"
        elif delta.seconds >= 7200:
            time_delta = str(int(delta.seconds/3600)) + " hours"
        elif delta.seconds > 3600:
            time_delta = str(int(delta.seconds/3600)) + " hour"
        elif delta.seconds >= 120:
            time_delta = str(int(delta.seconds/60)) + " minutes"
        elif delta.seconds > 60:
            time_delta = str(int(delta.seconds/60)) + " minute"
        elif delta.seconds >= 2:
            time_delta = str(int(delta.seconds)) + " seconds"
        else:
            time_delta = str(int(delta.seconds)) + " second"
        return time_delta


def get_request_candidates(feedback_request):
    request_candidates = []
    # Feedbacker not assigned yet
    if feedback_request.feedbacker == feedback_request.feedbackee:
        request_candidates = FeedbackerCandidate.objects.filter(feedback=feedback_request)
    return request_candidates


def has_premium(user):
    curr_user = UserProfile.objects.get(user=user)
    return curr_user.premium
