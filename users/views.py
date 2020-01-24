from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages                             # Django built-in message alerts
from django.contrib.auth.decorators import login_required       # Django built-in login_required decorator
from .forms import UserRegistrationForm, EditUserForm, EditProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from main.models import Rating


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
            return render(request, 'users/email_confirmation.html')

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
        messages.success(request, f"Account created for {username}! You are now able to log in.")
        return redirect('login-page')      # redirects the user to the login page
    else:
        return render(request, 'users/email_confirmation_invalid.html')


@login_required
def customize_user_profile(request):
    if request.method == 'POST':
        u_form = EditUserForm(request.POST, instance=request.user)
        # will populate the form with the current user information by passing an instance parameter
        p_form = EditProfileForm(request.POST, request.FILES,  instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():        # check whether both forms are valid
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('profile-page')  # redirects the user to the profile page to avoid POST-GET-REDIRECT PATTERN
            # https://stackoverflow.com/questions/10827242/understanding-the-post-redirect-get-pattern
    else:
        u_form = EditUserForm(instance=request.user)
        p_form = EditProfileForm(instance=request.user.userprofile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/customize_profile.html', context=context)


@login_required
def view_profile(request):

    # Main purpose of separate apps is reuseability
    # This creates some sort of loose dependence between the main app and the users app (to be fixed 2 lines below)
    username = request.GET.get('user', '')
    user_to_view = User.objects.filter(username=username).first()

    if not user_to_view:                    # establish the independence of the app again
        user_to_view = request.user         # get the the currently logged in user

    ratings = Rating.objects.filter(feedbacker=user_to_view)
    context = {
        'user_to_view': user_to_view,
        'user_ratings': ratings
    }
    return render(request, 'users/view-profile.html', context)
    
    
#settings page
@login_required
def user_settings(request):
    return render(request, 'user/user-settings.html', context)
    
