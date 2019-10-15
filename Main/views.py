from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import FeedbackRequest
from .forms import UserRegistrationForm
from .forms import NewFeedbackRequestForm

def home(request):
    if not request.user.is_authenticated:
        return redirect('login-page')
    context = {
        'requests' : FeedbackRequest.objects.all()
    }
    return render(request,'feedback_requests.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    context = {
        'wronglogin' : False,
        'form' : UserRegistrationForm()
    }
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
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-page')
        else:
            context['wronglogin'] = True
    return render(request,'register.html',context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login-page')
    context = {
        'user_name' : request.user.username,
        'my_requests' : FeedbackRequest.objects.filter(feedbackee=request.user)
    }
    return render(request,'profile.html',context)

def new_feedback_request(request):
    if not request.user.is_authenticated:
        return redirect('login-page')
    if request.method == "POST":
        form = NewFeedbackRequestForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            maintext = form.cleaned_data['maintext']
            reward = form.cleaned_data['reward']
            feedback_request = FeedbackRequest(title=title,maintext=maintext,feedbackee=request.user,reward=reward,feedbacker=request.user)
            feedback_request.save()
            return redirect('home-page')
        else:
            print("INVALID")
    return render(request,'new_feedback_request.html')

def feedback_request(request):
    request_id = request.GET.get('request_id','')
    if request_id != "":
        context = {
            'feedback_request' : FeedbackRequest.objects.get(id=request_id)
        }
        return render(request,'feedback_request.html',context)
    else:
        return redirect('home-page')
