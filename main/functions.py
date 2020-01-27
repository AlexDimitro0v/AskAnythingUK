from .models import FeedbackRequest
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from users.models import UserProfile

def get_time_delta(time_0,time_1):
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
        print("here")
        curr_request_candidates_ids = FeedbackRequest.objects.raw(
            '''SELECT main_feedbackercandidate.feedbacker_id AS id
               FROM main_feedbackercandidate
               INNER JOIN main_feedbackrequest
               ON main_feedbackercandidate.feedback_id = main_feedbackrequest.id
               WHERE main_feedbackercandidate.feedback_id=%s
            ''', [feedback_request.id])
        curr_request_candidates_ids = [curr_candidate.id for curr_candidate in curr_request_candidates_ids]
        request_candidates = User.objects.filter(pk__in=set(curr_request_candidates_ids))
    return request_candidates

def has_premium(user):
    curr_user = UserProfile.objects.get(user=user)
    return datetime.now(timezone.utc) <= curr_user.premium_ends
