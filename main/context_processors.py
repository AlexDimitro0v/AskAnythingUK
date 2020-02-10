from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from .models import Notification, Area
from .functions import get_time_delta, has_premium
from django.contrib.auth.decorators import login_required

def notifications_processor(request):
     if not request.user.is_authenticated:
        return {}
     notifications = []
     curr_time = datetime.now(timezone.utc)
     for n in Notification.objects.filter(user=request.user).order_by('-date'):
         notification = {
             "type": n.type,
             "title": n.feedback_request,
             "link": "http://localhost:8000/feedback-request/?request_id="+str(n.feedback_request.id),
             "time": get_time_delta(n.date, curr_time),
             "other_user": n.other_user
         }
         notifications.append(notification)
     return {'notifications_all': notifications}


def logged_in_universal_processor(request):
    if not request.user.is_authenticated:
        return {}
    context = {
        'areas':  Area.objects.all(),
        'has_premium': has_premium(request.user)
    }
    return context
