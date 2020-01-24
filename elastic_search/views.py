from django.shortcuts import render
from .documents import FeedbackRequestDocument
from django.db.models import F        # used to compare 2 instances or fields of the same model
from main.models import Area
from django.core.paginator import Paginator

def search(request):

    query = request.GET.get('q')

    requests = None
    if query:
        requests = FeedbackRequestDocument.search().query("multi_match", query=query, fields=['title', 'maintext'])
        requests = requests.to_queryset()
        requests = requests.filter(feedbackee=F('feedbacker')).exclude(feedbackee=request.user)

        page_number = request.GET.get('page', 1)        # defaults to 1 if not found
        paginator = Paginator(requests, 5)     # each page contains 5 feedback requests
        requests = paginator.get_page(page_number)
        page_obj = requests

    context = {
        'requests' : requests,
        'search' : query,
        'areas' :  Area.objects.all(),
        'page_obj' : page_obj
    }

    return render(request, 'main/search-requests.html', context)
