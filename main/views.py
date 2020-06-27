from django.shortcuts import redirect

def home(request):
    return redirect('http://www.realaskanything.com/')


def handler404(request, *args, **kwargs):
    return redirect('http://www.realaskanything.com/')


def handler500(request, *args, **kwargs):
    return redirect('http://www.realaskanything.com/')
