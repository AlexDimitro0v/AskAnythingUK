from django.shortcuts import render, redirect
from .models import FeedbackRequest, FeedbackerCandidate, Category, Tag, Rating
from .forms import NewFeedbackRequestForm, FeedbackerCommentsForm, FeedbackerRatingForm
from django.contrib import messages   # Django built-in message alerts
from django.db.models import F        # used to compare 2 instances or fields of the same model
# https://books.agiliq.com/projects/django-orm-cookbook/en/latest/f_query.html

from django.db import connections
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

import datetime

@login_required
def home(request):
    # # Only allow logged-in users to view feedback requests
    # if not request.user.is_authenticated:
    #     return redirect('login-page')

    # Get the tag filter, return an empty string if not found:
    tag_filter = request.GET.get('tag-filter', '')      # https://stackoverflow.com/a/49872199
    if tag_filter == "":
        # Get all requests that do not have an assigned feedbacker by checking if feedbackee = feedbacker
        # (excluding the requests from the currently logged in user)
        # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/f_query.html
        feedback_requests = FeedbackRequest.objects.filter(feedbackee=F('feedbacker')).exclude(feedbackee=request.user)
    else:
        # If tag-filter in the url (e.g. http://127.0.0.1:8000/?tag-filter=Writing) a dic will be created
        # {tag-filter: Writing} and all the requests will be filtered in accordance to this tag
        #
        # https://stackoverflow.com/a/49872199

        # https://docs.djangoproject.com/en/3.0/topics/db/sql/ - useful explanation of raw
        # Get all requests that have the selected tag-filter only,
        # excluding the requests from the currently logged in user:
        feedback_requests = FeedbackRequest.objects.raw(''' SELECT main_tag.feedback_id AS id
                                                            FROM main_tag
                                                            INNER JOIN main_category ON main_tag.category_id = main_category.id
                                                            INNER JOIN main_feedbackrequest ON main_tag.feedback_id = main_feedbackrequest.id
                                                            WHERE main_category.name=%s
                                                            AND main_feedbackrequest.feedbacker_id = main_feedbackrequest.feedbackee_id
                                                            AND main_feedbackrequest.feedbacker_id != %s
                                                            ''', [tag_filter, request.user.id])
    # Create a list of tags for each feedback request
    tags = []   # will contain nested lists of tag names
    for feedback_request in feedback_requests:
        # Note: Have a look at the models folder to have a clear idea about the entities below:
        request_tag_ids = Tag.objects.filter(feedback=feedback_request)   # get all tags from the feedback requests list
        request_tags = [tag.category for tag in request_tag_ids]          # get all tag categories instances
        tags.append([tag.name for tag in request_tags])                   # finally store the name of those categories

    context = {
        'requests': feedback_requests,
        'tags': tags
    }
    return render(request, 'main/feedback_requests.html', context)


@login_required
def dashboard(request):
    # # Only logged-in users can view their own dashboard
    # if not request.user.is_authenticated:
    #     return redirect('login-page')

    my_feedbacker_applications_ids = FeedbackerCandidate.objects.values_list('feedback', flat=True).filter(
        feedbacker=request.user)
    my_feedbacker_applications = FeedbackRequest.objects.filter(pk__in=set(my_feedbacker_applications_ids))
    my_feedback_requests = FeedbackRequest.objects.filter(feedbackee=request.user)

    feedback_candidates = []
    for my_request in my_feedback_requests:
        curr_request_candidates = []
        # Feedbacker not assigned yet
        if my_request.feedbacker == my_request.feedbackee:
            curr_request_candidates_ids = FeedbackRequest.objects.raw(
                'SELECT main_feedbackercandidate.feedbacker_id AS id FROM main_feedbackercandidate INNER JOIN main_feedbackrequest ON main_feedbackercandidate.feedback_id = main_feedbackrequest.id  WHERE main_feedbackercandidate.feedback_id=%s',
                [my_request.id])
            curr_request_candidates_ids = [curr_candidate.id for curr_candidate in curr_request_candidates_ids]
            curr_request_candidates = User.objects.filter(pk__in=set(curr_request_candidates_ids))
        feedback_candidates.append(curr_request_candidates)

    context = {
        'my_requests': my_feedback_requests,            # Feedback Request instances
        'my_applications': my_feedbacker_applications,  # Feedback Request instances
        'feedback_candidates': feedback_candidates,     # User instances
        # 'feedbacker_info': Feedbacker.objects.filter(user=request.user).first()
    }
    return render(request, 'main/dashboard.html', context)


@login_required
def new_feedback_request(request):
    # # Only logged-in users can make new requests
    # if not request.user.is_authenticated:
    #     return redirect('login-page')

    # If new feedback request form just sent
    if request.method == "POST":
        form = NewFeedbackRequestForm(request.POST)

        # Get all tags attached to request and remove potential duplicates
        tags = list(set(request.GET.get('tags', '').split(",")))

        if form.is_valid():
            # Save feedback request to database if data is valid
            title = form.cleaned_data['title']
            maintext = form.cleaned_data['maintext']
            reward = form.cleaned_data['reward']
            time_limit = form.cleaned_data['timelimit']
            feedback_request = FeedbackRequest(title=title, maintext=maintext, feedbackee=request.user, reward=reward,
                                               feedbacker=request.user, time_limit=time_limit)
            feedback_request.save()

            # Save each attached zip file
            feedbackZIPFile = request.FILES['fileZip']
            fs = FileSystemStorage()
            fs.save('zip_files/' + str(feedback_request.id) + '.zip', feedbackZIPFile)

            # Save each tag instance to database
            for tag in tags:
                category_record = Category.objects.filter(name=tag)
                if not category_record:
                    category_record = Category(name=tag)
                    category_record.save()
                else:
                    category_record = category_record[0]
                tag_record = Tag(feedback=feedback_request, category=category_record)
                tag_record.save()
            return redirect('home-page')

    return render(request, 'main/new_feedback_request.html')


@login_required
def feedback_request(request):
    # # Only logged-in users can view feedback requests
    # if not request.user.is_authenticated:
    #     return redirect('login-page')

    request_id = request.GET.get('request_id', '')
    user_is_feedbacker = False
    user_is_candidate = False
    user_is_feedbackee = False
    user_was_rejected = False

    feedbackee_files_link = None
    feedbacker_files_link = None

    fs = FileSystemStorage()

    # User is feedbackee for this request
    if FeedbackRequest.objects.get(id=request_id).feedbackee == request.user:
        user_is_feedbackee = True
        feedbackee_files_link = fs.url('zip_files/' + request_id+".zip")
        if fs.exists('zip_files/' + request_id+"_feedbacker.zip"):
            feedbacker_files_link = fs.url('zip_files/' + request_id+"_feedbacker.zip")
    # User is feedbacker for this request
    elif FeedbackRequest.objects.get(id=request_id).feedbacker == request.user:
        user_is_feedbacker = True
        feedbackee_files_link = fs.url('zip_files/' + request_id+".zip")
        if fs.exists('zip_files/' + request_id+"_feedbacker.zip"):
            feedbacker_files_link = fs.url('zip_files/' + request_id+"_feedbacker.zip")
    # User is candidate for this request
    elif FeedbackerCandidate.objects.filter(feedbacker=request.user, feedback_id=request_id).first():
        if FeedbackRequest.objects.get(id=request_id).feedbackee != FeedbackRequest.objects.get(id=request_id).feedbacker:
            user_was_rejected = True
        else:
            user_is_candidate = True
    if request_id != "":
        context = {
            'feedback_request': FeedbackRequest.objects.get(id=request_id),
            'request_id': request_id,
            'user_is_candidate': user_is_candidate,
            'user_is_feedbacker': user_is_feedbacker,
            'feedbackee_files_link': feedbackee_files_link,
            'feedbacker_files_link': feedbacker_files_link,
            'user_is_feedbackee': user_is_feedbackee,
            'user_was_rejected': user_was_rejected
        }
        return render(request, 'main/feedback_request.html', context)
    else:
        return redirect('home-page')


@login_required
def apply_as_feedbacker(request):
    # if not request.user.is_authenticated:
    #     return redirect('login-page')

    feedback_request_id = request.GET.get('request_id', '')
    feedback_request = FeedbackRequest.objects.get(id=feedback_request_id)
    cursor = connections['default'].cursor()
    cursor.execute("INSERT INTO main_feedbackercandidate (feedbacker_id,feedback_id) VALUES( %s , %s )",
                   [request.user.id, feedback_request_id])
    cursor.close()
    messages.success(request, f"Your application has been processed!")
    return redirect('dashboard')


# @login_required
# def feedbacker_profile(request):
#     # ASK STEPAN ABOUT ALL OF THE VALIDATIONS AND REDIRECTS TO THE PROFILE-PAGE
#
#     # if not request.user.is_authenticated:
#     #     return redirect('login-page')
#     feedbacker_username = request.GET.get('user', '')
#     feedback_request_id = request.GET.get('feedback', '')
#
#     # Get feedbacker from database
#     feedbacker = User.objects.filter(username=feedbacker_username)
#     if feedbacker:
#         feedbacker = feedbacker[0]
#     else:
#         return redirect('profile-page')       # change to redirect to dashboard if in use again !!!!!!!!!!!!!
#     my_feedback_requests = FeedbackRequest.objects.filter(feedbackee=request.user, id=feedback_request_id)
#
#     if not my_feedback_requests:
#         return redirect('profile-page')
#
#     candidates = FeedbackerCandidate.objects.filter(feedback=feedback_request_id)
#
#     if not candidates:
#         return redirect('profile-page')
#     feedbacker_is_candidate = False
#     for candidate in candidates:
#         if candidate.feedbacker == feedbacker:
#             feedbacker_is_candidate = True
#
#     if not feedbacker_is_candidate:
#         return redirect('profile-page')
#
#     context = {
#         'feedbacker': feedbacker,
#     }
#     return render(request, 'main/feedbacker-profile.html', context)


# def customize_profile(request):
#     if not request.user.is_authenticated:
#         return redirect('login-page')
#
#     if request.method == "POST":
#         form = FedbackerProfileForm(request.POST)
#         if form.is_valid():
#             existing_feedbacker = Feedbacker.objects.filter(user=request.user).first()
#             if existing_feedbacker != None:
#                 existing_ssssprofile_description = form.cleaned_data['description']
#                 existing_feedbacker.save()
#             else:
#                 feedbacker = Feedbacker(user=request.user, profile_description=form.cleaned_data['description'])
#                 feedbacker.save()
#             return redirect('profile-page')       # change to redirect to dashboard if in use again !!!!!!!!!!!!!
#
#     profile_description = str()
#     if Feedbacker.objects.filter(user=request.user).first():
#         profile_description = Feedbacker.objects.filter(user=request.user).first().profile_description
#     context = {
#         'prev_description': profile_description
#     }
#     return render(request, 'customize_profile.html', context)


@login_required
def choose_feedbacker(request):
    # if not request.user.is_authenticated:
    #     return redirect('login-page')

    feedbacker_username = request.GET.get('user', '')
    feedback_request_id = request.GET.get('feedback', '')
    feedback_request = FeedbackRequest.objects.filter(id=feedback_request_id).first()
    feedback_request.feedbacker = User.objects.filter(username=feedbacker_username).first()
    feedback_request.save()
    messages.success(request, f"Feedbacker has been chosen successfully!")
    return redirect('dashboard')


def submit_feedback(request):
    if not request.user.is_authenticated:
        return redirect('login-page')

    if request.method == "POST":
        request_id = request.GET.get('request_id', '')
        form = FeedbackerCommentsForm(request.POST)

        if form.is_valid():
            comments = form.cleaned_data['comments']

            feedback_request = FeedbackRequest.objects.get(id=request_id)

            # Capping an error (just in case)
            if(feedback_request.feedbacker != request.user or feedback_request.feedbacker == feedback_request.feedbackee):
                messages.error(request, "An error has occurred!")
                return redirect('home-page')

            feedback_request.feedbacker_comments = comments
            feedback_request.date_completed = datetime.datetime.now()
            feedback_request.save()

            feedbackZIPFile = request.FILES['fileZip']
            fs = FileSystemStorage()
            fs.save('zip_files/' + str(feedback_request.id) + '_feedbacker.zip', feedbackZIPFile)
            messages.success(request, "Feedback submitted!")
            return redirect('dashboard')

    context = {
        'request_id': request.GET.get('request_id', '')
    }
    return render(request, 'main/submit_feedback.html', context)

@login_required
def rate_feedbacker(request):
    request_id = request.GET.get('request_id','')
    if not request_id:
        return redirect('dashboard')

    feedback_request = FeedbackRequest.objects.get(id=request_id)

    if feedback_request.feedbackee != request.user or feedback_request.date_posted == feedback_request.date_completed or feedback_request.feedbacker_rated:
        return redirect('dashboard')

    if request.method == "POST":
        form = FeedbackerRatingForm(request.POST)

        if form.is_valid():
            review = form.cleaned_data['review']
            quality = form.cleaned_data['quality']
            speed = form.cleaned_data['speed']
            communication = form.cleaned_data['communication']
            rating = Rating(review=review, quality=quality, speed=speed, communication=communication, feedbackee=request.user,
                                               feedbacker=feedback_request.feedbacker)
            rating.save()

            feedback_request.feedbacker_rated = 1
            feedback_request.save()
            
            return redirect('dashboard')

    context = {
        'request_id': request.GET.get('request_id', '')
    }
    return render(request,'main/rate-feedbacker.html',context)
