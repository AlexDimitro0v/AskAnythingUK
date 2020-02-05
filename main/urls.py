from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home-page"),
    path('landing-page/', views.landing_page, name="landing-page"),
    path('feedback-requests/', views.feedback_requests, name="feedback-requests-page"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('new-feedback-request/', views.new_feedback_request, name="new-feedback-request-page"),
    path('feedback-request/', views.feedback_request, name="feedback-request-page"),
    path('apply-as-feedbacker/', views.apply_as_feedbacker, name="apply-as-feedbacker-page"),
    path('choose-feedbacker/', views.choose_feedbacker, name="choose-feedbacker-page"),
    path('submit-feedback/', views.submit_feedback, name="submit-feedback-page"),
    path('rate-feedbacker/', views.rate_feedbacker, name="rate-feedbacker-page"),
    path('withdraw-application/', views.withdraw_application, name="withdraw-application-page"),
    path('feedback-request/<int:pk>/delete', views.RequestDeleteView.as_view(template_name='main/feedback_request_delete.html'),
         name='request-delete'),
    path('finish-purchase/', views.finish_purchase, name='finish-purchase'),
    path('get-new-messages/', views.get_new_messages, name='get-new-messages')

]
