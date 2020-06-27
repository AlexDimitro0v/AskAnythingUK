from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home-page"),
]
handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
