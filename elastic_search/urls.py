from django.urls import path
from . import views

urlpatterns = [
    path('search-requests/', views.search, name="search-page"),
]
