from datetime import datetime
from django.shortcuts import render, redirect
from .models import FeedbackRequest, FeedbackerCandidate, Category, Tag, Rating, Area, Purchase, Message
from .forms import NewFeedbackRequestForm, FeedbackerCommentsForm, FeedbackerRatingForm, ApplicationForm, MessageForm
from django.contrib import messages   # Django built-in message alerts
from django.db.models import F        # used to compare 2 instances or fields of the same model
from django.core.paginator import Paginator
from django.db import connections
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max
from django.db.models import Min
from django.db.models.expressions import RawSQL
from .functions import get_time_delta, get_request_candidates, has_premium
from AskAnything.settings import BRAINTREE_PUBLIC_KEY, BRAINTREE_PRIVATE_KEY, BRAINTREE_MERCHANT_KEY
import braintree
import json
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.views.generic import (
    DeleteView
)
# Class-based views types:
# ListView    — to view the list of objects
# CreateView  — to create a particular object
# DetailView  — to view a particular object
# UpdateView  — to update a particular object
# DeleteView  — to delete a particular object

# Set up the payment gateway
braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=BRAINTREE_MERCHANT_KEY,
                                  public_key=BRAINTREE_PUBLIC_KEY,
                                  private_key=BRAINTREE_PRIVATE_KEY)

# =====================================================================================================================
# FUNCTION-BASED VIEWS:


# Redirect unauthenticated users to landing page
@login_required(login_url='landing-page')
def home(request):
    context = {
        'areas':  Area.objects.all(),
        'has_premium': has_premium(request.user)
    }
    return render(request, 'main/home.html', context)


def landing_page(request):
    return render(request, 'main/home.html')


@login_required
def feedback_requests(request):
    # Get the tag filter, return an empty string if not found:
    tag_filter = request.GET.get('tag-filter', '')      # https://stackoverflow.com/a/49872199
    area_filter = request.GET.get('area-filter', '')
    filtered_min_price = request.GET.get('min-price', '')
    filtered_max_price = request.GET.get('max-price', '')
    filtered_min_time = request.GET.get('min-time', '')
    filtered_max_time = request.GET.get('max-time', '')

    if not area_filter:
        return redirect('home-page')

    area = Area.objects.get(id=area_filter)

    # Get all requests that do not have an assigned feedbacker by checking if feedbackee = feedbacker
    # (excluding the requests from the currently logged in user)
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/f_query.html
    feedback_requests = FeedbackRequest.objects.filter(feedbackee=F('feedbacker'), area=area).exclude(feedbackee=request.user)

    # Exclude all requests for which the user has already applied
    my_feedbacker_applications_ids = FeedbackerCandidate.objects.values_list('feedback', flat=True).filter(feedbacker=request.user)
    feedback_requests = feedback_requests.exclude(pk__in=set(my_feedbacker_applications_ids))

    # Get minimum and maximum values of price and time limit for all feedback requests in a given category
    max_price = feedback_requests.aggregate(Max('reward'))['reward__max']
    min_price = feedback_requests.aggregate(Min('reward'))['reward__min']
    max_time = feedback_requests.aggregate(Max('time_limit'))['time_limit__max']
    min_time = feedback_requests.aggregate(Min('time_limit'))['time_limit__min']

    most_used_tags = []

    # No tag filter specified
    if tag_filter == "":

        # Filter requests if min/max price or time specified
        if filtered_min_price:
            feedback_requests = FeedbackRequest.objects.filter(feedbackee=F('feedbacker'),
                                                               area=area,
                                                               reward__lte=filtered_max_price,
                                                               reward__gte=filtered_min_price,
                                                               time_limit__gte=filtered_min_time,
                                                               time_limit__lte=filtered_max_time).exclude(feedbackee=request.user)

        # Aggregate all popular tags in the specified category
        # TODO Optimize the code below. What if there are thousands of tags?
        # Solution: Get the tags only from the feedback requests on the current page
        all_used_tags = {}
        for feedback_request in feedback_requests:
            request_tag_ids = Tag.objects.filter(feedback=feedback_request)
            request_tags = [tag.category for tag in request_tag_ids]
            for tag in request_tags:
                if tag in all_used_tags:
                    all_used_tags[tag] += 1
                else:
                    all_used_tags[tag] = 1

        # Sort tags from most to least used
        sorted_tags = sorted(all_used_tags.items(), key=lambda kv: -kv[1])

        # Take 10 most popular tags
        if len(sorted_tags) > 10:
            sorted_tags = sorted_tags[:10]
        for tag in sorted_tags:                     # iterate through the list of tuples
            most_used_tags.append(tag[0])           # get the key from the kvp

    else:
        # If tag-filter in the url (e.g. http://127.0.0.1:8000/?tag-filter=Writing) a dic will be created
        # {tag-filter: Writing} and all the requests will be filtered in accordance to this tag
        #
        # https://stackoverflow.com/a/49872199

        if not filtered_max_time:
            filtered_min_price = min_price
            filtered_max_price = max_price
            filtered_min_time = min_time
            filtered_max_time = max_time

        # https://docs.djangoproject.com/en/3.0/topics/db/sql/ - useful explanation of raw
        # Get all requests that have the selected tag-filter only,
        # excluding the requests from the currently logged in user:
        feedback_requests = FeedbackRequest.objects.filter(id__in=RawSQL(''' SELECT main_tag.feedback_id AS id
                                                            FROM main_tag
                                                            INNER JOIN main_category ON main_tag.category_id = main_category.id
                                                            INNER JOIN main_feedbackrequest ON main_tag.feedback_id = main_feedbackrequest.id
                                                            WHERE main_category.name=%s
                                                            AND main_feedbackrequest.feedbacker_id = main_feedbackrequest.feedbackee_id
                                                            AND main_feedbackrequest.feedbacker_id != %s
                                                            AND main_feedbackrequest.area_id = %s
                                                            AND main_feedbackrequest.reward >= %s
                                                            AND main_feedbackrequest.reward <= %s
                                                            AND main_feedbackrequest.time_limit >= %s
                                                            AND main_feedbackrequest.time_limit <= %s
                                                            ''', [tag_filter, request.user.id, area_filter, filtered_min_price,filtered_max_price, filtered_min_time, filtered_max_time]))

    feedback_requests = feedback_requests.exclude(pk__in=set(my_feedbacker_applications_ids))

    feedback_requests = feedback_requests.order_by('-date_posted')

    non_premium_requests = []
    premium_requests = []
    for feedback_request in feedback_requests:
        if has_premium(feedback_request.feedbackee):
            premium_requests.append(feedback_request)
        else:
            non_premium_requests.append(feedback_request)

    sorted_feedback_requests = []
    for i in range(len(feedback_requests)):
        if (i % 5 == 0 or i % 5 == 1) and premium_requests:
            sorted_feedback_requests.append(premium_requests.pop(0))
        else:
            if not premium_requests:
                sorted_feedback_requests.append(non_premium_requests.pop(0))
            elif not non_premium_requests:
                sorted_feedback_requests.append(premium_requests.pop(0))
            else:
                if premium_requests[0].date_posted >= non_premium_requests[0].date_posted:
                    sorted_feedback_requests.append(premium_requests.pop(0))
                else:
                    sorted_feedback_requests.append(non_premium_requests.pop(0))

    # Paginate:
    # https://docs.djangoproject.com/en/3.0/topics/pagination/
    page_number = request.GET.get('page', 1)               # defaults to 1 if not found
    paginator = Paginator(sorted_feedback_requests, 5)     # each page contains 5 feedback requests
    sorted_feedback_requests = paginator.get_page(page_number)
    page_obj = sorted_feedback_requests

    # Create a list of tags for each feedback request
    tags = []   # will contain nested lists of tag names
    for feedback_request in sorted_feedback_requests:
        # Note: Have a look at the models folder to have a clear idea about the entities below:
        request_tag_ids = Tag.objects.filter(feedback=feedback_request)   # get all tags from the feedback requests list
        request_tags = [tag.category for tag in request_tag_ids]          # get all tag categories instances
        tags.append([tag.name for tag in request_tags])                   # finally store the name of those categories


    time_deltas = []
    curr_time = datetime.now(timezone.utc)
    for feedback_request in sorted_feedback_requests:
        time_posted = feedback_request.date_posted
        time_deltas.append(get_time_delta(time_posted, curr_time))

    premium_requests = []
    for feedback_request in sorted_feedback_requests:
        if has_premium(feedback_request.feedbackee):
            premium_requests.append(True)
        else: premium_requests.append(False)

    new_requests = []
    for feedback_request in sorted_feedback_requests:
        if (datetime.now(timezone.utc) - feedback_request.date_posted).total_seconds() < 86400:
            new_requests.append(True)
        else: new_requests.append(False)

    context = {
        'requests': sorted_feedback_requests,
        'tags': tags,
        'page_obj': page_obj,
        'areas':  Area.objects.all(),
        'area_filter_id': int(area_filter),
        'tag_filter': tag_filter,
        'min_price': min_price,
        'max_price': max_price,
        'min_time': min_time,
        'max_time': max_time,
        'filtered_min_price': filtered_min_price,
        'filtered_max_price': filtered_max_price,
        'filtered_min_time': filtered_min_time,
        'filtered_max_time': filtered_max_time,
        'most_used_tags': most_used_tags,
        'time_deltas': time_deltas,
        'premium_requests': premium_requests,
        'new_requests': new_requests,
        'has_premium': has_premium(request.user),
        'title': '| Feedback Requests'
    }

    return render(request, 'main/feedback_requests.html', context)


@login_required
def dashboard(request):
    my_feedbacker_applications_ids = FeedbackerCandidate.objects.values_list('feedback', flat=True).filter(
        feedbacker=request.user)
    my_feedbacker_applications = FeedbackRequest.objects.filter(pk__in=set(my_feedbacker_applications_ids)).exclude(feedbacker=request.user)
    my_feedback_requests = FeedbackRequest.objects.filter(feedbackee=request.user)
    my_jobs = FeedbackRequest.objects.filter(feedbacker=request.user).exclude(feedbackee=F("feedbacker"))

    fs = FileSystemStorage()
    times_left = []
    urgent = []
    curr_time = datetime.now(timezone.utc)
    for job in my_jobs:
        if fs.exists('zip_files/' + str(job.id) +"_feedbacker.zip"):
            times_left.append(-1)
            urgent.append(False)
        else:
            deadline = job.date_started + timedelta(days=job.time_limit)

            # Urgent jobs have less than one day left to submit feedback
            if curr_time + timedelta(days=1) > deadline:
                urgent.append(True)
            else:
                urgent.append(False)

            if curr_time > deadline:
                times_left.append(0)
            else:
                times_left.append(get_time_delta(curr_time,deadline))

    feedback_candidates = []
    for my_request in my_feedback_requests:
        num_of_candidates = len(get_request_candidates(my_request))
        if num_of_candidates < 1:
            feedback_candidates.append(None)
        elif num_of_candidates == 1:
            feedback_candidates.append("1 Feedbacker Candidate")
        else:
            feedback_candidates.append(str(num_of_candidates) + " Feedbacker Candidates")

    context = {
        'my_requests': my_feedback_requests,            # Feedback Request instances
        'my_applications': my_feedbacker_applications,  # Feedback Request instances
        'my_jobs': my_jobs,
        'feedback_candidates': feedback_candidates,     # User instances
        'areas':  Area.objects.all(),
        'has_premium': has_premium(request.user),
        'times_left': times_left,
        'urgent': urgent,
        'title': '| Dashboard'
    }
    return render(request, 'main/dashboard.html', context)


@login_required
def new_feedback_request(request):
    # If new feedback request form just sent
    if request.method == "POST":
        form = NewFeedbackRequestForm(request.POST)

        # Get all tags attached to request and remove potential duplicates
        tags = list(set(request.GET.get('tags', '').split(",")))
        if form.is_valid():

            # Save feedback request to database if data is valid
            title = form.cleaned_data['title']
            area_id = form.cleaned_data['area']
            maintext = form.cleaned_data['maintext']
            reward = form.cleaned_data['reward']
            time_limit = form.cleaned_data['timelimit']

            area = Area.objects.get(id=area_id)

            feedback_request = FeedbackRequest(area=area,
                                               title=title,
                                               maintext=maintext,
                                               feedbackee=request.user,
                                               reward=reward,
                                               feedbacker=request.user,
                                               time_limit=time_limit
                                               )
            feedback_request.save()

            # Save each attached zip file
            feedbackZIPFile = request.FILES['fileZip']
            fs = FileSystemStorage()
            fs.save('zip_files/' + str(feedback_request.id) + '.zip', feedbackZIPFile)

            # Save each tag instance to database
            for tag in tags:
                if tag == "":
                    continue
                category_record = Category.objects.filter(name=tag)
                if not category_record:
                    category_record = Category(name=tag)
                    category_record.save()
                else:
                    category_record = category_record[0]
                tag_record = Tag(feedback=feedback_request, category=category_record)
                tag_record.save()

    #       return redirect('home-page')

    areas = Area.objects.all()
    context = {
        "areas": areas,
        'has_premium': has_premium(request.user),
        'title': '| New Feedback Request'
        }
    return render(request, 'main/new_feedback_request.html', context)


@login_required
def feedback_request(request):
    request_id = request.GET.get('request_id', '')
    user_is_feedbacker = False
    user_is_candidate = False
    user_is_feedbackee = False
    user_was_rejected = False

    feedbackee_files_link = None
    feedbacker_files_link = None

    feedback_request = FeedbackRequest.objects.get(id=request_id)

    feedback_candidates = get_request_candidates(feedback_request)

    candidate_premiums = []
    for candidate in feedback_candidates:
        candidate_premiums.append(has_premium(candidate.feedbacker))

    curr_time = datetime.now(timezone.utc)
    time_posted = feedback_request.date_posted
    time_delta = get_time_delta(time_posted, curr_time)

    premium_request = False
    if has_premium(feedback_request.feedbackee):
                premium_request = True

    new_request = False
    if (datetime.now(timezone.utc) - feedback_request.date_posted).total_seconds() < 86400:
        new_request = True

    # Count the number of active applications the user has
    num_of_applications = 0
    if not has_premium(request.user):
        applications = FeedbackerCandidate.objects.filter(feedbacker=request.user)
        for application in applications:
            if application.feedback.feedbackee == application.feedback.feedbacker:
                num_of_applications +=1

    fs = FileSystemStorage()

    # User is feedbackee for this request
    if feedback_request.feedbackee == request.user:
        user_is_feedbackee = True
        feedbackee_files_link = fs.url('zip_files/' + request_id+".zip")
        if fs.exists('zip_files/' + request_id+"_feedbacker.zip"):
            feedbacker_files_link = fs.url('zip_files/' + request_id+"_feedbacker.zip")
    # User is feedbacker for this request
    elif feedback_request.feedbacker == request.user:
        user_is_feedbacker = True
        feedbackee_files_link = fs.url('zip_files/' + request_id+".zip")
        if fs.exists('zip_files/' + request_id+"_feedbacker.zip"):
            feedbacker_files_link = fs.url('zip_files/' + request_id+"_feedbacker.zip")
    # User is candidate for this request
    elif FeedbackerCandidate.objects.filter(feedbacker=request.user, feedback_id=request_id).first():
        if feedback_request.feedbackee != feedback_request.feedbacker:
            user_was_rejected = True
        else:
            user_is_candidate = True

    if feedback_request.feedbackee != feedback_request.feedbacker and not user_is_feedbackee and not user_is_feedbacker and not user_was_rejected:
        return redirect('dashboard')

    # New message
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message_text = form.cleaned_data['message']
            message = Message(message=message_text, feedback_id=request_id, author=request.user)
            message.save()
            if user_is_feedbacker and feedback_request.feedbackee.is_authenticated:
                feedback_request.new_feedbacker_message = True
                feedback_request.save()
            elif user_is_feedbackee and feedback_request.feedbacker.is_authenticated:
                feedback_request.new_feedbackee_message = True
                feedback_request.save()

            return redirect('home-page')

    messages = Message.objects.filter(feedback_id=request_id)
    messages.order_by('-date')

    latest_user_message_date = None
    if messages:
        latest_user_message_date = messages.latest('date').date.strftime("%Y-%m-%d %H:%M:%S.%f")
    client_tokens = [braintree.ClientToken.generate() for candidate in feedback_candidates]
    if request_id != "":
        context = {
            'feedback_request': feedback_request,
            'request_id': request_id,
            'user_is_candidate': user_is_candidate,
            'user_is_feedbacker': user_is_feedbacker,
            'feedbackee_files_link': feedbackee_files_link,
            'feedbacker_files_link': feedbacker_files_link,
            'user_is_feedbackee': user_is_feedbackee,
            'user_was_rejected': user_was_rejected,
            'time_delta': time_delta,
            'areas':  Area.objects.all(),
            'feedback_candidates': feedback_candidates,
            'date_posted': feedback_request.date_posted.replace(microsecond=0),
            'date_completed': feedback_request.date_completed.replace(microsecond=0),
            'has_premium': has_premium(request.user),
            'new_request': new_request,
            'premium_request': premium_request,
            'three_or_more_applications': num_of_applications >= 3,
            'client_tokens': client_tokens,
            'purchase': Purchase.objects.filter(feedback=feedback_request).first(),
            'feedbackee_has_premium': has_premium(feedback_request.feedbackee),
            'feedbacker_has_premium': has_premium(feedback_request.feedbacker),
            'candidate_premiums': candidate_premiums,
            'title': '| ' + feedback_request.title,
            'user_messages': messages,
            'latest_user_message_date': latest_user_message_date
        }
        return render(request, 'main/feedback_request.html', context)
    else:
        return redirect('home-page')


@login_required
def apply_as_feedbacker(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)

        if form.is_valid():
            feedback_request_id = request.GET.get('request_id', '')
            feedback_request = FeedbackRequest.objects.get(id=feedback_request_id)

            # Feedbacker already chosen, cannot apply
            if feedback_request.feedbacker != feedback_request.feedbackee:
                return redirect('dashboard')

            # Cannot apply twice to the same feedback request
            past_application = FeedbackerCandidate.objects.filter(feedbacker=request.user, feedback=feedback_request)
            if past_application:
                return redirect('dashboard')

            application_text = form.cleaned_data['application']

            application = FeedbackerCandidate(feedbacker=request.user,
                                              feedback=feedback_request,
                                              application=application_text,
                                              )
            application.save()
            current_site = get_current_site(request)                        # get current site
            mail_subject = 'New candidate for your feedback request'
            to_email = feedback_request.feedbackee.email
            message = f"Hi, {feedback_request.feedbackee},\nYou have a new candidate for your Request: '{feedback_request}'." \
                      f"\n\nLogin to see the updates:\nhttp://{current_site}\n\nThank you for using our service,\n" \
                      f"Your AskAnything team."
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            if feedback_request.feedbackee.userprofile.notifications:
                email.send()

            messages.success(request, f"Your application has been processed!")
    return redirect('dashboard')


@login_required
def choose_feedbacker(request):
    if request.method == 'POST':
        try:
            feedback_request = FeedbackRequest.objects.get(id=request.POST['feedback_request_id'])
            if feedback_request.feedbackee != request.user or feedback_request.feedbackee != feedback_request.feedbacker:
                return redirect('dashboard')
            feedbacker = User.objects.get(username=request.POST['feedbacker_username'])
        except FeedbackRequest.DoesNotExist:
            return redirect('/')

        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": feedback_request.reward,
            "payment_method_nonce": nonce
        })

        if result.is_success:
            feedback_request.feedbacker = feedbacker
            feedback_request.date_started = datetime.now(timezone.utc)
            feedback_request.save()
            purchase = Purchase(
                feedback=feedback_request,
                feedbackee=feedback_request.feedbackee,
                feedbacker=feedbacker,
                time=datetime.now(tz=timezone.utc)
            )
            purchase.save()

            current_site = get_current_site(request)                        # get current site
            mail_subject = f"AskAnything"
            to_email = feedback_request.feedbacker.email
            message = f"Hi, {feedback_request.feedbacker},\n{feedback_request.feebackee} has chosen you as a feedbacker" \
                      f"for '{feedback_request}'.\n\n" \
                      f"Login to see the updates:\nhttp://{current_site}\n\nThank you for using our service,\n" \
                      f"Your AskAnything team."
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            if feedback_request.feedbacker.userprofile.notifications:
                email.send()

            messages.success(request, f"Feedbacker has been chosen successfully!")
        else:
            messages.error(request, f"Problem with payment method")

    return redirect('dashboard')


@login_required
def submit_feedback(request):
    request_id = request.GET.get('request_id', '')
    try:
        feedback_request = FeedbackRequest.objects.get(id=request_id)
    except:
        return redirect('dashboard')

    # Only the feedbacker of the request can submit feedback
    if(feedback_request.feedbacker != request.user or feedback_request.feedbacker == feedback_request.feedbackee):
            messages.error(request, "An error has occurred!")
            return redirect('dashboard')

    if request.method == "POST":
        request_id = request.GET.get('request_id', '')
        form = FeedbackerCommentsForm(request.POST)

        if form.is_valid():
            comments = form.cleaned_data['comments']

            # Default value
            if comments == "":
                comments = "-"

            feedback_request.feedbacker_comments = comments

            feedback_request.date_completed = datetime.now(tz=timezone.utc)
            feedback_request.save()

            current_site = get_current_site(request)                        # get current site
            message = f"Hi, {feedback_request.feedbackee},\nYou have received feedback." \
                      f"for your request: '{feedback_request}'.\n\n" \
                      f"Login to see the updates:\nhttp://{current_site}\n\nThank you for using our service,\n" \
                      f"Your AskAnything team."
            mail_subject = 'You received feedback.'
            to_email = feedback_request.feedbackee.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            if feedback_request.feedbackee.userprofile.notifications:
                email.send()

            feedbackZIPFile = request.FILES['fileZip']
            fs = FileSystemStorage()
            # Delete any previously submitted feedback
            fs.delete('zip_files/' + str(feedback_request.id) + '_feedbacker.zip')
            fs.save('zip_files/' + str(feedback_request.id) + '_feedbacker.zip', feedbackZIPFile)
            messages.success(request, "Feedback submitted!")
            return redirect('dashboard')

    context = {
        'request_id': request.GET.get('request_id', ''),
        'areas':  Area.objects.all(),
        'has_premium': has_premium(request.user),
        'title': '| Submit Feedback',
        'feedbacker_comments': feedback_request.feedbacker_comments
    }
    return render(request, 'main/submit_feedback.html', context)


@login_required
def rate_feedbacker(request):
    request_id = request.GET.get('request_id', '')
    if not request_id:
        return redirect('dashboard')

    feedback_request = FeedbackRequest.objects.get(id=request_id)

    if feedback_request.feedbackee != request.user or feedback_request.date_posted.replace(microsecond=0) == feedback_request.date_completed.replace(microsecond=0) or feedback_request.feedbacker_rated:
        return redirect('dashboard')

    if request.method == "POST":
        form = FeedbackerRatingForm(request.POST)

        if form.is_valid():
            overall = form.cleaned_data['overall']
            review = form.cleaned_data['review']
            quality = form.cleaned_data['quality']
            speed = form.cleaned_data['speed']
            communication = form.cleaned_data['communication']
            rating = Rating(review=review, overall=overall, quality=quality, speed=speed, communication=communication, feedbackee=request.user,
                                               feedbacker=feedback_request.feedbacker)
            rating.save()

            current_site = get_current_site(request)  # get current site
            message = f"Hi, {feedback_request.feedbacker},\nYou have been rated for your work on." \
                      f": '{feedback_request}'.\n\n" \
                      f"Login to see the updates:\nhttp://{current_site}\n\nThank you for using our service,\n" \
                      f"Your AskAnything team."
            mail_subject = 'You have been rated.'
            to_email = feedback_request.feedbacker.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            if feedback_request.feedbacker.userprofile.notifications:
                email.send()
            feedback_request.feedbacker_rated = True
            feedback_request.save()
            messages.success(request, 'You have successfully rated your feedbacker!')
            return redirect('dashboard')

    context = {
        'request_id': request.GET.get('request_id', ''),
        'areas':  Area.objects.all(),
        'has_premium': has_premium(request.user),
        'title': '| Rate Feedbacker'
    }
    return render(request, 'main/rate-feedbacker.html', context)


@login_required
def withdraw_application(request):
    feedback_request_id = request.GET.get('request_id', '')

    application = FeedbackerCandidate.objects.get(feedbacker=request.user, feedback_id=feedback_request_id)
    application.delete()
    messages.success(request, f"Your application has been withdrawn!")
    return redirect('dashboard')


@login_required
def finish_purchase(request):
    feedback_request_id = request.GET.get('feedback_request', '')
    feedback_request = FeedbackRequest.objects.get(id=feedback_request_id)
    try:
        purchase = Purchase.objects.get(feedback=feedback_request_id)
    except:
        raise Exception('This request simply does not have a Purchase instance, i.e. it is an old request. Try'
                        'creating one manually via the admin panel.')
    purchase.is_completed = True
    purchase.save()
    return redirect('dashboard')


@login_required
def get_new_messages(request):
    request_id = request.GET.get('request_id', '')
    if not request_id:
        return redirect('dashboard')

    feedback_request = FeedbackRequest.objects.get(id=request_id)
    if request.is_ajax():
        latest_user_message_date = request.POST.get('latest_user_message_date', None)

        if feedback_request.feedbackee == request.user and feedback_request.new_feedbacker_message:
            feedback_request.new_feedbacker_message = False
            feedback_request.save()

            messages = Message.objects.filter(feedback_id=request_id,author=feedback_request.feedbacker,date__gt=latest_user_message_date)
            messages.order_by('-date')

            message_texts = []
            for message in messages:
                message_texts.append(message.message)

            return HttpResponse(json.dumps({'has_premium': has_premium(feedback_request.feedbacker),'messages': message_texts,'newestMessage': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}), content_type="application/json")
        if feedback_request.feedbacker == request.user and feedback_request.new_feedbackee_message:
            feedback_request.new_feedbackee_message = False
            feedback_request.save()

            messages = Message.objects.filter(feedback_id=request_id,author=feedback_request.feedbackee,date__gt=latest_user_message_date)
            messages.order_by('-date')

            message_texts = []
            for message in messages:
                message_texts.append(message.message)

            return HttpResponse(json.dumps({'has_premium': has_premium(feedback_request.feedbackee),'messages': message_texts,'newestMessage': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}), content_type="application/json")
        return HttpResponse(json.dumps(None), content_type="application/json")

# =====================================================================================================================


# =====================================================================================================================
# CLASS-BASED VIEWS:
class RequestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    By default Django expects a template that is just a form that asks if we are sure that we want to delete the request
    and if we submit the form, the request will be deleted. Django also looks for a template named:
    <app>/<model>_confirm_delete.html, i.e. main/feedbackrequest_confirm_delete.html by default.
    """
    model = FeedbackRequest         # which model to query in order to delete a request
    # template_name = 'main/feedback_request_delete.html'

    def test_func(self):
        """
        The function put a restriction on deleting other's users feedback requests.
        The currently logged-in user must NOT be able to delete other's people feedback requests or requests that have
        already been assigned to a feedbacker.
        This is when a user try to write the url manually.
        """
        feedback_request = self.get_object()     # get the exact feedback_request to be currently deleted

        if self.request.user == feedback_request.feedbackee and feedback_request.feedbackee == feedback_request.feedbacker:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and deletes the adequate feedback request + the zip file.
        """
        feedback_request = self.get_object()     # get the exact feedback_request to be currently deleted
        if self.request.user == feedback_request.feedbackee and feedback_request.feedbackee == feedback_request.feedbacker:
            fs = FileSystemStorage()
            fs.delete('zip_files/' + str(feedback_request.id) + '.zip')
            feedback_request.delete()
            messages.success(request, 'You have successfully deleted your feedback request.')
            return redirect('dashboard')
        else:
            raise Http404
