from django.shortcuts import render, redirect
from django.contrib import messages              # Django built-in message alerts
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, EditUserForm
from django.contrib.auth.models import User


def register(request):
    context = {

        'title': 'Register',
    }

    # If registration POST request just sent
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()                     # sends the data to the database
            # process the data in form.cleaned_data as required:
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You are now able to log in.")
            return redirect('login-page')   # redirects the user to the login page
    else:
        form = UserRegistrationForm()

    context['form'] = form

    return render(request, 'users/register.html', context)


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

    # Get user from database (establishing the independence of the app again)
    user_to_view = User.objects.filter(username=username).first()
    if not user_to_view:
        user_to_view = request.user         # get the the currently logged in user

    context = {
        'user_to_view': user_to_view,
    }
    return render(request, 'users/view-profile.html', context)
