from datetime import datetime
from django.shortcuts import render, redirect
from .models import FeedbackRequest, FeedbackerCandidate, Category, Tag, Rating, Area, Purchase, Message, Notification
from .forms import NewFeedbackRequestForm, FeedbackerCommentsForm, FeedbackerRatingForm, ApplicationForm, MessageForm
from django.db.models import F        # used to compare 2 instances or fields of the same model
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
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
import main.notifications as notifications
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
import sweetify
from .user_agents import save_device_info, check_for_fraud
from .smart_recommendations import get_most_common, get_recommended_feedbackers
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
    return render(request, 'main/home.html')


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
    try:
        area = Area.objects.get(id=area_filter)
    except:
        # Area does not exist
        return redirect('home-page')

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
        else:
            premium_requests.append(False)

    new_requests = []
    for feedback_request in sorted_feedback_requests:
        if (datetime.now(timezone.utc) - feedback_request.date_posted).total_seconds() < 86400:
            new_requests.append(True)
        else: new_requests.append(False)

    context = {
        'requests': sorted_feedback_requests,
        'tags': tags,
        'page_obj': page_obj,
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
        'title': '| Feedback Requests'
    }

    return render(request, 'main/feedback_requests.html', context)


@login_required
def dashboard(request):
    my_feedbacker_applications_ids = FeedbackerCandidate.objects.values_list('feedback', flat=True).filter(
        feedbacker=request.user)
    my_feedbacker_applications = FeedbackRequest.objects.filter(pk__in=set(my_feedbacker_applications_ids)).exclude(feedbacker=request.user)

    my_feedback_requests = []
    for feedback_request in FeedbackRequest.objects.filter(feedbackee=request.user).order_by('-date_posted'):
        try:
            if not (feedback_request.feedbacker_rated and Purchase.objects.get(feedback=feedback_request).is_completed):
                my_feedback_requests.append(feedback_request)
        except:
            my_feedback_requests.append(feedback_request)

    my_jobs = []
    for job in FeedbackRequest.objects.filter(feedbacker=request.user).exclude(feedbackee=F("feedbacker")).order_by('-date_started'):
        try:
            if not (job.feedbacker_rated and Purchase.objects.get(feedback=job).is_completed):
                my_jobs.append(job)
        except:
            my_jobs.append(job)

    times_left = []
    urgent = []
    curr_time = datetime.now(timezone.utc)
    for job in my_jobs:
        if job.feedbacker_comments != "":
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
        'times_left': times_left,
        'urgent': urgent,
        'title': '| Dashboard'
    }
    return render(request, 'main/dashboard.html', context)


@login_required
def archive(request):
    archived_requests = []
    for feedback_request in FeedbackRequest.objects.filter(feedbackee=request.user,feedbacker_rated=True):
        try:
            if Purchase.objects.get(feedback=feedback_request).is_completed:
                archived_requests.append(feedback_request)
        except:
            pass

    archived_jobs = []
    for job in FeedbackRequest.objects.filter(feedbacker=request.user,feedbacker_rated=True):
        try:
            if Purchase.objects.get(feedback=job).is_completed:
                archived_jobs.append(job)
        except:
            pass

    context = {
        'archived_requests': archived_requests,            # Feedback Request instances
        'archived_jobs': archived_jobs,
        'title': '| Archive'
    }

    return render(request, 'main/archive.html', context)


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
            most_common = get_most_common(maintext)
            most_common_words = []
            most_common_words_numbers = []
            for w in most_common:
                most_common_words.append(w[0])
                most_common_words_numbers.append(w[1])

            area = Area.objects.get(id=area_id)

            feedback_request = FeedbackRequest(area=area,
                                               title=title,
                                               maintext=maintext,
                                               feedbackee=request.user,
                                               reward=reward,
                                               feedbacker=request.user,
                                               time_limit=time_limit,
                                               most_common_words=most_common_words,
                                               most_common_words_numbers=most_common_words_numbers
                                               )
            feedback_request.save()

            recommended_users = get_recommended_feedbackers(most_common_words, most_common_words_numbers)
            for u in recommended_users:
                if not u == request.user:
                    notifications.recommended_request_notification(feedback_request, get_current_site(request), u)

            # Save each attached zip file
            feedbackZIPFile = request.FILES['fileZip']
            fs = default_storage.open('zip_files/' + str(feedback_request.id) + '.zip', 'w')
            fs.write(feedbackZIPFile)
            fs.save()
            fs.close()

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

    context = {
        'title': '| New Feedback Request'
        }
    return render(request, 'main/new_feedback_request.html', context)


@login_required
def feedback_request(request):
    notification_id = request.GET.get('notification_id', '')
    if notification_id:
        try:
            notification = Notification.objects.get(id=notification_id)
            if notification.user == request.user:
                notification.seen = True
                notification.save()
        except:
            pass

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
                num_of_applications += 1

    fs = default_storage

    # User is feedbackee for this request
    if feedback_request.feedbackee == request.user:
        user_is_feedbackee = True
        file = default_storage.url('zip_files/' + request_id+".zip")
        feedbackee_files_link = file
        if fs.exists('zip_files/' + request_id+"_feedbacker.zip"):
            file = default_storage.url(
                'zip_files/' + request_id + "_feedbacker.zip")

            feedbacker_files_link = file
    # User is feedbacker for this request
    elif feedback_request.feedbacker == request.user:
        user_is_feedbacker = True

        file = default_storage.url('zip_files/' + request_id+".zip")
        feedbackee_files_link = file
        if fs.exists('zip_files/' + request_id+"_feedbacker.zip"):
            file = default_storage.url(
                'zip_files/' + request_id + "_feedbacker.zip")

            feedbacker_files_link = file
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
            if user_is_feedbacker:
                if feedback_request.feedbackee.userprofile.is_online:
                    feedback_request.new_feedbacker_message = True
                    feedback_request.save()
                else:
                    notifications.new_message_notification(feedback_request, get_current_site(request), feedback_request.feedbacker, feedback_request.feedbackee)

            elif user_is_feedbackee:
                if feedback_request.feedbacker.userprofile.is_online:
                    feedback_request.new_feedbackee_message = True
                    feedback_request.save()
                else:
                    notifications.new_message_notification(feedback_request, get_current_site(request), feedback_request.feedbackee, feedback_request.feedbacker)

            return redirect('home-page')

    messages = Message.objects.filter(feedback_id=request_id)
    messages.order_by('-date')

    latest_user_message_date = None
    if messages:
        latest_user_message_date = messages.latest('date').date.strftime("%Y-%m-%d %H:%M:%S.%f")
    try:
        if request.user.userprofile.payment_method:
            braintree_client_token = braintree.ClientToken.generate({"customer_id": request.user.username})
        else:
            braintree_client_token = braintree.ClientToken.generate({})
    except:
        braintree_client_token = braintree.ClientToken.generate({})

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
            'feedback_candidates': feedback_candidates,
            'date_posted': feedback_request.date_posted.replace(microsecond=0),
            'date_completed': feedback_request.date_completed.replace(microsecond=0),
            'new_request': new_request,
            'premium_request': premium_request,
            'three_or_more_applications': num_of_applications >= 3,
            'client_token': braintree_client_token,
            'purchase': Purchase.objects.filter(feedback=feedback_request).first(),
            'feedbackee_has_premium': has_premium(feedback_request.feedbackee),
            'feedbacker_has_premium': has_premium(feedback_request.feedbacker),
            'candidate_premiums': candidate_premiums,
            'title': '| ' + feedback_request.title,
            'user_messages': messages,
            'latest_user_message_date': latest_user_message_date,
            'feedbacker_reward': feedback_request.feedbacker_reward,
            'charity_reward': feedback_request.charity_reward,
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
            proposed_reward = form.cleaned_data['proposed_reward']

            application = FeedbackerCandidate(feedbacker=request.user,
                                              feedback=feedback_request,
                                              application=application_text,
                                              proposed_reward=proposed_reward
                                              )
            application.save()

            notifications.new_candidate_notification(feedback_request, get_current_site(request), request.user)

            sweetify.success(request, 'Your application has been processed!', icon='success', toast=True,
                             position='bottom-end',
                             padding='1.5rem'
                             )
    return redirect('dashboard')


@login_required
def choose_feedbacker(request):
    if request.method == 'POST':
        try:
            feedback_request_id = request.POST['feedback_request_id']
            feedback_request = FeedbackRequest.objects.get(id=feedback_request_id)
            if feedback_request.feedbackee != request.user or feedback_request.feedbackee != feedback_request.feedbacker:
                return redirect('dashboard')
            feedbacker = User.objects.get(username=request.POST['feedbacker_username'])
        except FeedbackRequest.DoesNotExist:
            return redirect('/')

        application = FeedbackerCandidate.objects.get(feedbacker=feedbacker, feedback_id=feedback_request_id)
        if(application.proposed_reward):
            reward = application.proposed_reward
            feedback_request.reward = reward
        else:
            reward = feedback_request.reward

        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": reward,
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

            notifications.chosen_as_feedbacker_notification(feedback_request, get_current_site(request))

        else:
            sweetify.error(request, 'Problem with payment method', icon="error", toast=True, position="bottom-end",
                           padding='1.5rem')

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

            notifications.feedback_submitted_notification(feedback_request, get_current_site(request))

            feedbackZIPFile = request.FILES['fileZip']
            fs = default_storage
            # Delete any previously submitted feedback
            fs.delete('zip_files/' + str(feedback_request.id) + '_feedbacker.zip')

            # Save the new one
            fs = default_storage.open('zip_files/' + str(feedback_request.id) + '_feedbacker.zip', 'w')
            fs.write(feedbackZIPFile)
            fs.close()
            return redirect('dashboard')

    context = {
        'request_id': request.GET.get('request_id', ''),
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

            # Save device info of the reviewer
            user_device = save_device_info(request)
            if user_device:
                if check_for_fraud(feedback_request.feedbacker,user_device):
                    print("Probably a fake review")

            notifications.feedbacker_rated_notification(feedback_request, get_current_site(request))

            feedback_request.feedbacker_rated = True
            feedback_request.save()
            sweetify.success(request, 'You have successfully rated your feedbacker!', icon='success', toast=True,
                             position='bottom-end',
                             padding='1.5rem'
                             )
            return redirect('dashboard')

    context = {
        'request_id': request.GET.get('request_id', ''),
        'title': '| Rate Feedbacker'
    }
    return render(request, 'main/rate-feedbacker.html', context)


@login_required
def withdraw_application(request):
    feedback_request_id = request.GET.get('request_id', '')

    application = FeedbackerCandidate.objects.get(feedbacker=request.user, feedback_id=feedback_request_id)
    application.delete()
    sweetify.success(request, "Your application has been withdrawn", icon='success', toast=True, position='bottom-end',
                     padding='1.5rem'
                     )
    return redirect('dashboard')


@login_required
def finish_purchase(request):
    feedback_request_id = request.GET.get('feedback_request', '')
    feedback_request = FeedbackRequest.objects.get(id=feedback_request_id)
    feedbacker_reward = int(request.GET.get('feedbacker_reward', feedback_request.reward))
    charity_reward = int(request.GET.get('charity_reward', 0))

    try:
        purchase = Purchase.objects.get(feedback=feedback_request_id)
    except:
        raise Exception('This request simply does not have a Purchase instance, i.e. it is an old request. Try'
                        'creating one manually via the admin panel.')
    purchase.is_completed = True
    feedback_request.feedbacker_reward = feedbacker_reward
    feedback_request.charity_reward = charity_reward

    feedback_request.save()
    purchase.save()

    notifications.money_released_notification(feedback_request, get_current_site(request))
    sweetify.success(request, "Reward released", icon='success', toast=True, position='bottom-end', padding='1.5rem')
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

            messages = Message.objects.filter(feedback_id=request_id, author=feedback_request.feedbacker, date__gt=latest_user_message_date)
            messages.order_by('-date')

            message_texts = []
            for message in messages:
                message_texts.append(message.message)

            return HttpResponse(json.dumps({'has_premium': has_premium(feedback_request.feedbacker), 'messages': message_texts,'newestMessage': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}), content_type="application/json")
        if feedback_request.feedbacker == request.user and feedback_request.new_feedbackee_message:
            feedback_request.new_feedbackee_message = False
            feedback_request.save()

            messages = Message.objects.filter(feedback_id=request_id, author=feedback_request.feedbackee, date__gt=latest_user_message_date)
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
            fs = default_storage
            fs.delete('zip_files/' + str(feedback_request.id) + '.zip')
            feedback_request.delete()
            sweetify.success(request, "Feedback request deleted", icon='success', toast=True,
                             position='bottom-end',
                             padding='1.2rem'
                             )
            return redirect('dashboard')
        else:
            raise Http404
