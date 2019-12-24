from django.shortcuts import render, redirect
from django.contrib import messages              # Django built-in message alerts
from .forms import UserRegistrationForm


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
