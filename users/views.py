from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register(request):
    context = {
        'form': UserRegistrationForm(),
        'invalid_username' : None,
        'invalid_email' : None,
        'invalid_password1' : None,
        'invalid_password2' : None
    }

    # If registration POST request just sent
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-page')
        else:
            context['invalid_username'] = form["username"].errors
            context['invalid_email'] = form["email"].errors
            context['invalid_password1'] = form["password1"].errors
            context['invalid_password2'] = form["password2"].errors

    return render(request, 'users/register.html', context)
