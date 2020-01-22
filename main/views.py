from django.shortcuts import render, redirect
from .models import FeedbackRequest, FeedbackerCandidate, Category, Tag, Rating, Area
from .forms import NewFeedbackRequestForm, FeedbackerCommentsForm, FeedbackerRatingForm
from django.contrib import messages   # Django built-in message alerts
from django.db.models import F        # used to compare 2 instances or fields of the same model
from django.core.paginator import Paginator
from django.db import connections
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import datetime
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DeleteView
)
from django.db.models import Max
from django.db.models import Min

# Class-based views types:
# ListView    — to view the list of objects
# CreateView  — to create a particular object
# DetailView  — to view a particular object
# UpdateView  — to update a particular object
# DeleteView  — to delete a particular object


# =====================================================================================================================
# FUNCTION-BASED VIEWS:
def home(request):
    # Redirect unauthenticated users to landing page
    if not request.user.is_authenticated:
        return redirect('landing-page')

    context = {
        'areas' :  Area.objects.all()
    }
    return render(request, 'main/home.html', context)




def landing_page(request):
    return render(request, 'main/landing-page.html')


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
    feedback_requests = FeedbackRequest.objects.filter(feedbackee=F('feedbacker'),area=area).exclude(feedbackee=request.user)

    # Get minimum and maximum values of price and time limit for all feedback requests in a given category
    max_price = feedback_requests.aggregate(Max('reward'))['reward__max']
    min_price = feedback_requests.aggregate(Min('reward'))['reward__min']
    max_time = feedback_requests.aggregate(Max('time_limit'))['time_limit__max']
    min_time = feedback_requests.aggregate(Min('time_limit'))['time_limit__min']

    if tag_filter == "":

        # Aggregate all popular tags in the specified category
        most_used_tags = []
        all_used_tags = {}
        for feedback_request in feedback_requests:
            request_tag_ids = Tag.objects.filter(feedback=feedback_request)
            request_tags = [tag.category for tag in request_tag_ids]
            for tag in request_tags:
                if tag in all_used_tags: all_used_tags[tag] += 1
                else: all_used_tags[tag] = 1

        # Sort tags from most to least used
        sorted_tags = sorted(all_used_tags.items(), key=lambda kv: -kv[1])

        # Take 10 most popular tags
        if len(sorted_tags) > 10:
            sorted_tags = sorted_tags[:10]

        for tag in sorted_tags:
            most_used_tags.append(tag[0])

        if filtered_min_price:
            feedback_requests = FeedbackRequest.objects.filter(feedbackee=F('feedbacker'),area=area,
                                                               reward__lte=filtered_max_price,
                                                               reward__gte=filtered_min_price,
                                                               time_limit__gte=filtered_min_time,
                                                               time_limit__lte=filtered_max_time).exclude(feedbackee=request.user)

        feedback_requests = feedback_requests.order_by('-date_posted')
        # https://docs.djangoproject.com/en/3.0/topics/pagination/
        page_number = request.GET.get('page', 1)        # defaults to 1 if not found
        paginator = Paginator(feedback_requests, 5)     # each page contains 5 feedback requests
        feedback_requests = paginator.get_page(page_number)
        page_obj = feedback_requests
    else:
        page_obj = None
        most_used_tags = None

        if not filtered_max_time:
            filtered_min_price = min_price
            filtered_max_price = max_price
            filtered_min_time = min_time
            filtered_max_time = max_time

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
                                                            AND main_feedbackrequest.area_id = %s
                                                            AND main_feedbackrequest.reward >= %s
                                                            AND main_feedbackrequest.reward <= %s
                                                            AND main_feedbackrequest.time_limit >= %s
                                                            AND main_feedbackrequest.time_limit <= %s
                                                            ''', [tag_filter, request.user.id, area_filter, filtered_min_price,filtered_max_price, filtered_min_time, filtered_max_time])

    # Create a list of tags for each feedback request
    tags = []   # will contain nested lists of tag names
    for feedback_request in feedback_requests:
        # Note: Have a look at the models folder to have a clear idea about the entities below:
        request_tag_ids = Tag.objects.filter(feedback=feedback_request)   # get all tags from the feedback requests list
        request_tags = [tag.category for tag in request_tag_ids]          # get all tag categories instances
        tags.append([tag.name for tag in request_tags])                   # finally store the name of those categories

    context = {
        'requests': feedback_requests,
        'tags': tags,
        'page_obj': page_obj,
        'areas' :  Area.objects.all(),
        'area_filter_id' : area_filter,
        'tag_filter' : tag_filter,
        'min_price' : min_price,
        'max_price' : max_price,
        'min_time' : min_time,
        'max_time' : max_time,
        'filtered_min_price' : filtered_min_price,
        'filtered_max_price' : filtered_max_price,
        'filtered_min_time' : filtered_min_time,
        'filtered_max_time' : filtered_max_time,
        'most_used_tags' : most_used_tags
    }

    return render(request, 'main/feedback_requests.html', context)


@login_required
def dashboard(request):
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
    # If new feedback request form just sent
    if request.method == "POST":
        form = NewFeedbackRequestForm(request.POST)

        # Get all tags attached to request and remove potential duplicates
        tags = list(set(request.GET.get('tags', '').split(",")))
        print(form)
        if form.is_valid():
            print("GORM")

            # Save feedback request to database if data is valid
            title = form.cleaned_data['title']
            area_id = form.cleaned_data['area']
            maintext = form.cleaned_data['maintext']
            reward = form.cleaned_data['reward']
            time_limit = form.cleaned_data['timelimit']

            area = Area.objects.get(id=area_id)

            feedback_request = FeedbackRequest(area=area,title=title, maintext=maintext, feedbackee=request.user, reward=reward,
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

    areas = Area.objects.all()
    context = {"areas" : areas}
    return render(request, 'main/new_feedback_request.html',context)


@login_required
def feedback_request(request):
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
    feedback_request_id = request.GET.get('request_id', '')
    feedback_request = FeedbackRequest.objects.get(id=feedback_request_id)
    cursor = connections['default'].cursor()
    cursor.execute("INSERT INTO main_feedbackercandidate (feedbacker_id,feedback_id) VALUES( %s , %s )",
                   [request.user.id, feedback_request_id])
    cursor.close()
    messages.success(request, f"Your application has been processed!")
    return redirect('dashboard')


@login_required
def choose_feedbacker(request):
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
            feedback_request.date_completed = datetime.datetime.now(tz=timezone.utc)
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
    request_id = request.GET.get('request_id', '')
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

            feedback_request.feedbacker_rated = True
            feedback_request.save()
            messages.success(request, 'You have successfully rated your feedbacker!')
            return redirect('dashboard')

    context = {
        'request_id': request.GET.get('request_id', '')
    }
    return render(request, 'main/rate-feedbacker.html', context)


@login_required
def withdraw_application(request):
    feedback_request_id = request.GET.get('request_id', '')

    application = FeedbackerCandidate.objects.get(feedbacker=request.user, feedback_id=feedback_request_id)
    application.delete()
    messages.success(request, f"Your application has been withdrawn!")
    return redirect('dashboard')

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
