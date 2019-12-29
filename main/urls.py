from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home-page"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('new-feedback-request/', views.new_feedback_request, name="new-feedback-request-page"),
    path('feedback-request/', views.feedback_request, name="feedback-request-page"),
    path('apply-as-feedbacker/', views.apply_as_feedbacker, name="apply-as-feedbacker-page"),
    # path('feedbacker-profile/', views.feedbacker_profile, name="feedbacker-profile-page"),
    # path('customize-profile/', views.customize_profile, name="customize-profile-page"),
    path('choose-feedbacker/', views.choose_feedbacker, name="choose-feedbacker-page"),
    path('submit-feedback/', views.submit_feedback, name="submit-feedback-page"),

]
