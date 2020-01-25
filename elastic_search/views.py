from django.shortcuts import render
from .documents import FeedbackRequestDocument
from django.db.models import F        # used to compare 2 instances or fields of the same model
from main.models import Area
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone
from main.functions import get_time_delta

def search(request):

    query = request.GET.get('q')

    requests = None
    time_deltas = []
    if query:
        requests = FeedbackRequestDocument.search().query("multi_match", query=query, fields=['title', 'maintext'])
        requests = requests.to_queryset()
        requests = requests.filter(feedbackee=F('feedbacker')).exclude(feedbackee=request.user)

        page_number = request.GET.get('page', 1)        # defaults to 1 if not found
        paginator = Paginator(requests, 5)     # each page contains 5 feedback requests
        requests = paginator.get_page(page_number)
        page_obj = requests

        curr_time = datetime.now(timezone.utc)
        for feedback_request in requests:
            time_posted = feedback_request.date_posted
            time_deltas.append(get_time_delta(time_posted,curr_time))

    context = {
        'requests' : requests,
        'search' : query,
        'areas' :  Area.objects.all(),
        'page_obj' : page_obj,
        'time_deltas' : time_deltas
    }

    return render(request, 'main/search-requests.html', context)
