from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name="home-page"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login-page"),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name="logout-page"),
    path('register/', views.register, name="registration-page"),
    path('profile/', views.profile, name="profile-page"),
    path('new-feedback-request/', views.new_feedback_request, name="new-feedback-request-page"),
    path('feedback-request/', views.feedback_request, name="feedback-request-page"),
    path('apply-as-feedbacker/', views.apply_as_feedbacker, name="apply-as-feedbacker-page"),
    path('feedbacker-profile/', views.feedbacker_profile, name="feedbacker-profile-page"),
    path('customize-profile/', views.customize_profile, name="customize-profile-page"),
    path('choose-feedbacker/', views.choose_feedbacker, name="choose-feedbacker-page"),

]

# We cannot use this in production, serving static files with Django is not efficient
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
