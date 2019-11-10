from django.shortcuts import render, redirect
from .models import FeedbackRequest, FeedbackerCandidate, Category, Tag, Feedbacker
from .forms import NewFeedbackRequestForm, FedbackerProfileForm
from django.db.models import F

from django.db import connections
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


def home(request):
    # Only allow logged-in users to view feedback requests
    if not request.user.is_authenticated:
        return redirect('login-page')

    tag_filter = request.GET.get('tag-filter', '')
    if tag_filter == "":
        # Get all requests that do not have an assigned feedbacker
        feedback_requests = FeedbackRequest.objects.filter(feedbacker=F('feedbackee')).exclude(feedbackee=request.user)
    else:
        feedback_requests = FeedbackRequest.objects.raw(''' SELECT main_tag.feedback_id AS id
                                                            FROM main_tag
                                                            INNER JOIN main_category ON main_tag.category_id = main_category.id
                                                            INNER JOIN main_feedbackrequest ON main_tag.feedback_id = main_feedbackrequest.id
                                                            WHERE main_category.name=%s
                                                            AND main_feedbackrequest.feedbacker_id = main_feedbackrequest.feedbackee_id
                                                            AND main_feedbackrequest.feedbacker_id != %s
                                                            ''', [tag_filter, request.user.id])
    # Create a list of tags for each feedback request
    tags = []
    for feedback_request in feedback_requests:
        request_tag_ids = Tag.objects.filter(feedback=feedback_request)
        request_tags = [tag.category for tag in request_tag_ids]
        tags.append([tag.name for tag in request_tags])

    context = {
        'requests': feedback_requests,
        'tags': tags
    }
    return render(request, 'feedback_requests.html', context)


def profile(request):
    # Only logged-in users can view their own profile
    if not request.user.is_authenticated:
        return redirect('login-page')

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
        'user': request.user,
        'my_requests': my_feedback_requests,
        'my_applications': my_feedbacker_applications,
        'feedback_candidates': feedback_candidates,
        'feedbacker_info': Feedbacker.objects.filter(user=request.user).first()
    }
    return render(request, 'profile.html', context)


def new_feedback_request(request):
    # Only logged-in users can make new requests
    if not request.user.is_authenticated:
        return redirect('login-page')

    # If new feedback request form just sent
    if request.method == "POST":
        form = NewFeedbackRequestForm(request.POST)

        # Get all tags attached to request and remove potential duplicates
        tags = list(set(request.GET.get('tags', '').split(",")))

        # Save feedback request to database if data is valid
        if form.is_valid():
            title = form.cleaned_data['title']
            maintext = form.cleaned_data['maintext']
            reward = form.cleaned_data['reward']
            time_limit = form.cleaned_data['timelimit']
            feedback_request = FeedbackRequest(title=title, maintext=maintext, feedbackee=request.user, reward=reward,
                                               feedbacker=request.user, time_limit=time_limit)
            feedback_request.save()

            feedbackZIPFile = request.FILES['fileZip']

            fs = FileSystemStorage()
            fs.save(str(feedback_request.id) + '.zip', feedbackZIPFile)
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
    return render(request, 'new_feedback_request.html')


def feedback_request(request):
    # Only logged-in users can view feedback requests
    if not request.user.is_authenticated:
        return redirect('login-page')

    request_id = request.GET.get('request_id', '')
    user_is_feedbacker = False
    user_is_candidate = False
    user_is_feedbackee = False

    feedback_files_link = None

    if FeedbackRequest.objects.get(id=request_id).feedbackee == request.user:
        user_is_feedbackee = True
        fs = FileSystemStorage()
        feedback_files_link = fs.url(request_id+".zip")
    elif FeedbackRequest.objects.get(id=request_id).feedbacker == request.user:
        user_is_feedbacker = True
        fs = FileSystemStorage()
        feedback_files_link = fs.url(request_id+".zip")

    elif FeedbackerCandidate.objects.filter(feedbacker=request.user, feedback_id=request_id).first():
        user_is_candidate = True
    if request_id != "":
        context = {
            'feedback_request': FeedbackRequest.objects.get(id=request_id),
            'request_id': request_id,
            'user_is_candidate': user_is_candidate,
            'user_is_feedbacker': user_is_feedbacker,
            'feedback_files_link' : feedback_files_link,
            'user_is_feedbackee' : user_is_feedbackee
        }
        return render(request, 'feedback_request.html', context)
    else:
        return redirect('home-page')


def apply_as_feedbacker(request):
    if not request.user.is_authenticated:
        return redirect('login-page')

    feedback_request_id = request.GET.get('request_id', '')
    feedback_request = FeedbackRequest.objects.get(id=feedback_request_id)
    cursor = connections['default'].cursor()
    cursor.execute("INSERT INTO main_feedbackercandidate (feedbacker_id,feedback_id) VALUES( %s , %s )",
                   [request.user.id, feedback_request_id])
    cursor.close()
    return redirect('profile-page')


def feedbacker_profile(request):
    if not request.user.is_authenticated:
        return redirect('login-page')
    feedbacker_username = request.GET.get('user', '')
    feedback_request_id = request.GET.get('feedback', '')

    # Get feedbacker from database
    feedbacker = User.objects.filter(username=feedbacker_username)
    if feedbacker:
        feedbacker = feedbacker[0]
    else:
        return redirect('profile-page')
    my_feedback_requests = FeedbackRequest.objects.filter(feedbackee=request.user, id=feedback_request_id)

    if not my_feedback_requests:
        return redirect('profile-page')

    feedback_request_info = FeedbackerCandidate.objects.filter(feedback=feedback_request_id)

    if not feedback_request_info or not feedback_request_info[0].feedbacker == feedbacker:
        return redirect('profile-page')

    context = {
        'username': feedbacker.username,
        'feedbacker_info': Feedbacker.objects.filter(user=feedbacker).first()
    }
    return render(request, 'feedbacker-profile.html', context)


def customize_profile(request):
    if not request.user.is_authenticated:
        return redirect('login-page')

    if request.method == "POST":
        form = FedbackerProfileForm(request.POST)
        if form.is_valid():
            existing_feedbacker = Feedbacker.objects.filter(user=request.user).first()
            if existing_feedbacker != None:
                existing_feedbacker.profile_description = form.cleaned_data['description']
                existing_feedbacker.save()
            else:
                feedbacker = Feedbacker(user=request.user, profile_description=form.cleaned_data['description'])
                feedbacker.save()
            return redirect('profile-page')

    profile_description = Feedbacker.objects.filter(user=request.user).first().profile_description
    context = {
        'prev_description' : profile_description
    }
    return render(request, 'customize_profile.html', context)


def choose_feedbacker(request):
    if not request.user.is_authenticated:
        return redirect('login-page')

    feedbacker_username = request.GET.get('user', '')
    feedback_request_id = request.GET.get('feedback', '')
    feedback_request = FeedbackRequest.objects.filter(id=feedback_request_id).first()
    feedback_request.feedbacker = User.objects.filter(username=feedbacker_username).first()
    feedback_request.save()
    return redirect('profile-page')
