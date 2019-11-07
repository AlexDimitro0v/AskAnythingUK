from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


# Create your views here.
def login(request):
    # Logged-in users cannot access login page
    if request.user.is_authenticated:
        return redirect('home-page')

    context = {
        'wronglogin': False,
        'form': UserRegistrationForm()
    }

    # If login POST request sent
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-page')
        else:
            context['wronglogin'] = True
    return render(request, 'users/login.html', context)


def register(request):
    context = {
        'wronglogin': False,
        'form': UserRegistrationForm()
    }

    # If registration POST request just sent
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-page')
        else:
            context['wronglogin'] = True
    return render(request, 'users/register.html', context)
