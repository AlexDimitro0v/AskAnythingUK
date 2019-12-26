from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name="registration-page"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login-page"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout-page"),
    path('profile-page/', views.view_profile, name="profile-page"),
    path('customize-profile/', views.customize_user_profile, name="customize-profile-page"),
]
