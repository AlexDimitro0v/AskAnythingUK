from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home-page"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login-page"),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name="logout-page"),
    path('register/', views.register, name="registration-page"),
    path('profile/', views.profile, name="profile-page"),
    path('new-feedback-request/', views.new_feedback_request, name="new-feedback-request-page"),
    path('feedback-request/', views.feedback_request, name="feedback-request-page"),
    path('apply-as-feedbacker/', views.apply_as_feedbacker, name="apply-as-feedbacker-page"),
]
