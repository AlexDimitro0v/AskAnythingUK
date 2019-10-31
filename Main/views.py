from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import FeedbackRequest
from .models import FeedbackerCandidate
from .models import Category
from .models import Tag
from .models import Feedbacker
from .forms import UserRegistrationForm
from .forms import NewFeedbackRequestForm
from .forms import FedbackerProfileForm
from django.db.models import F

from django.db import connections
from django.contrib.auth.models import User

def home(request):
    # Only allow logged-in users to view feedback requests
    if not request.user.is_authenticated:
        return redirect('login-page')

    tag_filter = request.GET.get('tag-filter','')
    if tag_filter == "":
        # Get all requests that do not have an assigned feedbacker
        feedback_requests = FeedbackRequest.objects.filter(feedbacker=F('feedbackee'))
    else:
        feedback_requests = FeedbackRequest.objects.raw('SELECT main_tag.feedback_id AS id FROM main_tag INNER JOIN main_category ON main_tag.category_id = main_category.id INNER JOIN main_feedbackrequest ON main_tag.feedback_id = main_feedbackrequest.id  WHERE main_category.name=%s AND main_feedbackrequest.feedbacker_id = main_feedbackrequest.feedbackee_id',[tag_filter])

    # Create a list of tags for each feedback request
    tags = []
    for feedback_request in feedback_requests:
        request_tag_ids = Tag.objects.filter(feedback=feedback_request)
        request_tags = [tag.category for tag in request_tag_ids]
        tags.append([tag.name for tag in request_tags])

    context = {
        'requests' : feedback_requests,
        'tags' : tags
    }
    return render(request,'feedback_requests.html',context)

def login(request):
    # Logged-in users cannot access login page
    if request.user.is_authenticated:
        return redirect('home-page')

    context = {
        'wronglogin' : False,
        'form' : UserRegistrationForm()
    }

    # If login POST request sent
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-page')
        else:
            context['wronglogin'] = True
    return render(request,'login.html',context)

def register(request):
    context = {
        'wronglogin' : False,
        'form' : UserRegistrationForm()
    }

    # If registration POST request just sent
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-page')
        else:
            context['wronglogin'] = True
    return render(request,'register.html',context)

def profile(request):
    # Only logged-in users can view their own profile
    if not request.user.is_authenticated:
        return redirect('login-page')

    my_feedbacker_applications_ids = FeedbackerCandidate.objects.values_list('feedback',flat=True).filter(feedbacker=request.user)
    my_feedbacker_applications = FeedbackRequest.objects.filter(pk__in=set(my_feedbacker_applications_ids))
    my_feedback_requests = FeedbackRequest.objects.filter(feedbackee=request.user)
    feedback_candidates = []

    for my_request in my_feedback_requests:
        curr_request_candidates = []
        # Feedbacker not assigned yet
        if my_request.feedbacker == my_request.feedbackee:
            curr_request_candidates_ids =  FeedbackRequest.objects.raw('SELECT main_feedbackercandidate.feedbacker_id AS id FROM main_feedbackercandidate INNER JOIN main_feedbackrequest ON main_feedbackercandidate.feedback_id = main_feedbackrequest.id  WHERE main_feedbackercandidate.feedback_id=%s',[my_request.id])
            curr_request_candidates_ids = [curr_candidate.id for curr_candidate in curr_request_candidates_ids]
            curr_request_candidates = User.objects.filter(pk__in=set(curr_request_candidates_ids))
        feedback_candidates.append(curr_request_candidates)

    context = {
        'user' : request.user,
        'my_requests' : my_feedback_requests,
        'my_applications' : my_feedbacker_applications,
        'feedback_candidates' : feedback_candidates,
        'feedbacker_info' : Feedbacker.objects.filter(user=request.user).first()
    }
    return render(request,'profile.html',context)

def new_feedback_request(request):
    # Only logged-in users can make new requests
    if not request.user.is_authenticated:
        return redirect('login-page')

    # If new feedback request form just sent
    if request.method == "POST":
        form = NewFeedbackRequestForm(request.POST)

        # Get all tags attached to request and remove potential duplicates
        tags = list(set(request.GET.get('tags','').split(",")))

        # Save feedback request to database if data is valid
        if form.is_valid():
            title = form.cleaned_data['title']
            maintext = form.cleaned_data['maintext']
            reward = form.cleaned_data['reward']
            feedback_request = FeedbackRequest(title=title,maintext=maintext,feedbackee=request.user,reward=reward,feedbacker=request.user)
            feedback_request.save()

            # Save each tag instance to database
            for tag in tags:
                category_record = Category.objects.filter(name=tag)
                if not category_record:
                    category_record = Category(name=tag)
                    category_record.save()
                else:
                    category_record = category_record[0]
                tag_record = Tag(feedback=feedback_request,category=category_record)
                tag_record.save()

            return redirect('home-page')
    return render(request,'new_feedback_request.html')

def feedback_request(request):
    # Only logged-in users can view feedback requests
    if not request.user.is_authenticated:
        return redirect('login-page')

    request_id = request.GET.get('request_id','')
    user_is_feedbacker = False
    user_is_candidate = False
    if FeedbackRequest.objects.get(id=request_id).feedbacker == request.user:
        user_is_feedbacker = True
    elif FeedbackerCandidate.objects.filter(feedbacker=request.user,feedback_id=request_id).first():
        user_is_candidate = True
    if request_id != "":
        context = {
            'feedback_request' : FeedbackRequest.objects.get(id=request_id),
            'request_id' : request_id,
            'user_is_candidate' : user_is_candidate,
            'user_is_feedbacker' : user_is_feedbacker
        }
        return render(request,'feedback_request.html',context)
    else:
        return redirect('home-page')

def apply_as_feedbacker(request):
    if not request.user.is_authenticated:
        return redirect('login-page')

    feedback_request_id = request.GET.get('request_id','')
    feedback_request = FeedbackRequest.objects.get(id=feedback_request_id)
    cursor = connections['default'].cursor()
    cursor.execute("INSERT INTO main_feedbackercandidate (feedbacker_id,feedback_id) VALUES( %s , %s )", [request.user.id, feedback_request_id])
    cursor.close()
    return redirect('profile-page')

def feedbacker_profile(request):
    if not request.user.is_authenticated:
        return redirect('login-page')
    feedbacker_username = request.GET.get('user','')
    feedback_request_id = request.GET.get('feedback','')

    # Get feedbacker from database
    feedbacker = User.objects.filter(username=feedbacker_username)
    if feedbacker:
        feedbacker = feedbacker[0]
    else:
        return redirect('profile-page')
    my_feedback_requests = FeedbackRequest.objects.filter(feedbackee=request.user,id=feedback_request_id)

    if not my_feedback_requests:
        return redirect('profile-page')

    feedback_request_info = FeedbackerCandidate.objects.filter(feedback=feedback_request_id)

    if not feedback_request_info or not feedback_request_info[0].feedbacker == feedbacker:
        return redirect('profile-page')

    context = {
        'username' : feedbacker.username,
        'feedbacker_info' : Feedbacker.objects.filter(user=feedbacker).first()
    }
    return render(request,'feedbacker-profile.html',context)

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
                feedbacker = Feedbacker(user=request.user,profile_description=form.cleaned_data['description'])
                feedbacker.save()
            return redirect('profile-page')

    return render(request,'customize_profile.html')

def choose_feedbacker(request):
    if not request.user.is_authenticated:
        return redirect('login-page')

    feedbacker_username = request.GET.get('user','')
    feedback_request_id = request.GET.get('feedback','')
    feedback_request = FeedbackRequest.objects.filter(id=feedback_request_id).first()
    feedback_request.feedbacker = User.objects.filter(username=feedbacker_username).first()
    feedback_request.save()
    return redirect('profile-page')
