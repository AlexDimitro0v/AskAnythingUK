from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required       # Django built-in login_required decorator
from .forms import UserRegistrationForm, PrivateInformationForm, PublicInformationForm, NotificationsForm, ProfileImageForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from main.models import Rating, Area, FeedbackRequest, Category, FeedbackerCandidate
from dateutil.relativedelta import relativedelta
from .models import UserProfile, Specialism
from datetime import datetime
from django.utils import timezone
from main.functions import has_premium, get_time_delta
from django.db.models import F        # used to compare 2 instances or fields of the same model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import sweetify
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from main.smart_recommendations import get_most_common


def register(request):
    context = {
        'title': 'Register',
    }

    if request.user.is_authenticated:
        return redirect('home-page')

    # If registration POST request just sent
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()                                                     # sends the data to the database
            current_site = get_current_site(request)                        # get current site
            mail_subject = 'Activate your account.'
            message = render_to_string('users/acc_active_email.html', {     # create Message
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            sweetify.warning(request, 'Please verify your email address to complete the registration.',
                             buttons=False,
                             icon='warning'
                             )
            return redirect('landing-page')

    # if a GET (or any other method), create a blank form
    else:
        form = UserRegistrationForm()       # shows the user the registration form (redirection does not occur)

    context['form'] = form

    return render(request, 'users/register.html', context)


def activate(request, uidb64, token):
    """
    Sets the user to active after email confirmation upon registering.
    Active users are able to log in and use the website.
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)              # user is now logged in
        # return redirect('home-page')

        # process the data in form.cleaned_data as required:
        username = user.username
        sweetify.success(request, f"Account created for {username}! You are now able to log in.", icon='success',
                         toast=True,
                         position='bottom-end',
                         )
        return redirect('login-page')      # redirects the user to the login page
    else:
        sweetify.error(request, 'The email confirmation link is invalid.', icon="error", toast=True, position="bottom-end")
        return redirect('landing-page')


@login_required
def view_profile(request):

    # Main purpose of separate apps is reuseability
    # This creates some sort of loose dependence between the main app and the users app (to be fixed 2 lines below)
    user_id = request.GET.get('user', '')

    allow_access = False

    if not user_id:                    # establish the independence of the app again
        user_to_view = request.user         # get the the currently logged in user
        allow_access = True
    else:
        user_id = int(user_id)
        user_to_view = User.objects.filter(id=user_id).first()
        # User can always view their own profile
        if user_id == request.user.id:
            allow_access = True

    # Users can only access profiles of candidates to their feedback reqests
    # or their feedbackers
    if not allow_access:
        my_feedback_requests = FeedbackRequest.objects.filter(feedbackee=request.user)
        for feedback_request in my_feedback_requests:
            if feedback_request.feedbacker == request.user:
                allow_access = True
                break
            user_is_candidate = FeedbackerCandidate.objects.filter(feedbacker=user_to_view, feedback=feedback_request)
            if user_is_candidate:
                allow_access = True
                break

    if not allow_access:
        return redirect('dashboard')

    jobs_finished = len(FeedbackRequest.objects.filter(feedbacker=user_to_view).exclude(feedbacker_comments="").exclude(feedbackee=F('feedbacker')))

    user_skills_ids = Specialism.objects.filter(feedbacker=request.user)
    user_skills = [skill.category for skill in user_skills_ids]

    ratings = Rating.objects.filter(feedbacker=user_to_view)
    ratings.order_by('-date_posted')

    time_deltas = []
    curr_time = datetime.now(timezone.utc)
    for rating in ratings:
        time_posted = rating.date_posted
        time_deltas.append(get_time_delta(time_posted, curr_time))

    ratings_num = len(ratings)

    overall_average = 0
    speed_average = 0
    comm_average = 0
    quality_average = 0

    if ratings_num:
        for rating in ratings:
            overall_average += rating.overall
            speed_average += rating.speed
            comm_average += rating.communication
            quality_average += rating.quality

        overall_average /= ratings_num
        speed_average /= ratings_num
        comm_average /= ratings_num
        quality_average /= ratings_num

    context = {
        'user_to_view': user_to_view,
        'user_ratings': ratings,
        'viewed_has_premium': has_premium(user_to_view),
        'jobs_finished': jobs_finished,
        'user_skills': user_skills,
        'time_deltas': time_deltas,
        'overall_average': round(overall_average, 1),
        'speed_average': round(speed_average, 1),
        'quality_average': round(quality_average, 1),
        'comm_average': round(comm_average, 1),
        'ratings_num': ratings_num,
        'title': '| ' + user_to_view.username + "'s Profile"
    }
    return render(request, 'users/view-profile.html', context)


@login_required
def get_premium(request):
    if has_premium(request.user):
        return redirect('dashboard')

    context = {
        'areas':  Area.objects.all(),
        'has_premium': has_premium(request.user),
        'title': '| Get Premium'
    }
    return render(request, 'users/get-premium.html', context)


@login_required
def try_premium(request):
    curr_user = UserProfile.objects.get(user=request.user)
    if datetime.now(timezone.utc) > curr_user.premium_ends:
        plus_one_month = datetime.now(timezone.utc) + relativedelta(months=1)
        curr_user.premium_ends = plus_one_month
        sweetify.success(request, "Premium account activated!", icon='success',
                         toast=True,
                         position='bottom-end',
                         padding='1.5rem'
                         )
        curr_user.save()
    return redirect('dashboard')


@login_required
def settings(request):
    # Proper way to handle multiple forms:
    # https://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django
    # TODO: Use a look-up dictionary to optimize the code
    active = request.GET.get('tab', '')
    if request.method == 'POST':
        if 'password-change' in request.POST:
            change_password_form = PasswordChangeForm(request.user, request.POST, prefix='password-change')
            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)  # Important!
                # Otherwise the user’s auth session will be invalidated and she/he will have to log in again.
                sweetify.success(request, "You successfully changed your password", icon='success',
                                 toast=True,
                                 position='bottom-end',
                                 )
            private_info_form = PrivateInformationForm(instance=request.user.userprofile, prefix='private-info')
            public_info_form = PublicInformationForm(instance=request.user.userprofile, prefix='public-info')
            notifications_form = NotificationsForm(request.POST, instance=request.user.userprofile, prefix='notifications')
            image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.userprofile,
                                          prefix='profile-image')

        elif 'private-info' in request.POST:
            private_info_form = PrivateInformationForm(request.POST, instance=request.user.userprofile, prefix='private-info')
            if private_info_form.is_valid():
                private_info_form.save()
                sweetify.success(request, "You successfully updated your profile", icon='success',
                                 toast=True,
                                 position='bottom-end',
                                 )
            else:
                sweetify.error(request, 'Please correct the error below', icon="error", toast=True, position="bottom-end")

            change_password_form = PasswordChangeForm(request.user, prefix='password-change')
            public_info_form = PublicInformationForm(instance=request.user.userprofile, prefix='public-info')
            notifications_form = NotificationsForm(request.POST, instance=request.user.userprofile, prefix='notifications')
            image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.userprofile,
                                          prefix='profile-image')

        elif 'public-info-description' in request.POST:
            public_info_form = PublicInformationForm(request.POST, request.FILES, instance=request.user.userprofile, prefix='public-info')
            if public_info_form.is_valid():
                description = public_info_form.cleaned_data['description']
                public_info_form.save()

                most_common = get_most_common(description)
                most_common_words = []
                most_common_words_numbers = []
                for w in most_common:
                    most_common_words.append(w[0])
                    most_common_words_numbers.append(w[1])
                request.user.userprofile.most_common_words = most_common_words
                request.user.userprofile.most_common_words_numbers = most_common_words_numbers
                request.user.userprofile.save()
                sweetify.success(request, "You successfully updated your profile", icon='success',
                                 toast=True,
                                 position='bottom-end',
                                 )
            tags = list(set(request.GET.get('tags', '').split(",")))

            # Delete all previous skills
            Specialism.objects.filter(feedbacker=request.user).delete()

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
                tag_record = Specialism(feedbacker=request.user, category=category_record)
                tag_record.save()

            change_password_form = PasswordChangeForm(request.user, prefix='password-change')
            private_info_form = PrivateInformationForm(instance=request.user.userprofile, prefix='private-info')
            notifications_form = NotificationsForm(request.POST, instance=request.user.userprofile, prefix='notifications')
            image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.userprofile,
                                          prefix='profile-image')

        elif 'notifications' in request.POST:
            print(request.POST)
            notifications_form = NotificationsForm(request.POST, instance=request.user.userprofile, prefix='public-info')
            if notifications_form.is_valid():
                pass
            change_password_form = PasswordChangeForm(request.user, prefix='notifications')
            public_info_form = PublicInformationForm(instance=request.user.userprofile, prefix='public-info')
            private_info_form = PrivateInformationForm(instance=request.user.userprofile, prefix='private-info')
            image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.userprofile,
                                          prefix='profile-image')

        elif 'profile-image-x' in request.POST:
            image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.userprofile, prefix='profile-image')
            if image_form.is_valid():
                image_form.save()
            change_password_form = PasswordChangeForm(request.user, prefix='password-change')
            private_info_form = PrivateInformationForm(instance=request.user.userprofile, prefix='private-info')
            public_info_form = PublicInformationForm(instance=request.user.userprofile, prefix='public-info')
            notifications_form = NotificationsForm(request.POST, instance=request.user.userprofile,
                                                   prefix='notifications')
    else:
        change_password_form = PasswordChangeForm(request.user, prefix='password-change')
        private_info_form = PrivateInformationForm(instance=request.user.userprofile, prefix='private-info')
        public_info_form = PublicInformationForm(instance=request.user.userprofile, prefix='public-info')
        notifications_form = NotificationsForm(request.POST, instance=request.user.userprofile, prefix='notifications')
        image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.userprofile,
                                      prefix='profile-image')

    user_skills_ids = Specialism.objects.filter(feedbacker=request.user)
    user_skills = [str(skill.category) for skill in user_skills_ids]

    context = {'change_password_form': change_password_form,
               'private_info_form': private_info_form,
               'public_info_form': public_info_form,
               'notifications_form': notifications_form,
               'image_form': image_form,
               'active': active,
               'notifications': request.user.userprofile.notifications,
               'email': request.user.email,
               'user_skills': user_skills,
               'title': '| Settings'
               }
    return render(request, 'users/settings.html', context)


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.userprofile.is_online = True
    user.userprofile.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.userprofile.is_online = False
    user.userprofile.save()
