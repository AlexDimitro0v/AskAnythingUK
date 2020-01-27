from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('register/', views.register, name="registration-page"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name="login-page"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout-page"),
    path('profile-page/', views.view_profile, name="profile-page"),
    path('customize-profile/', views.customize_user_profile, name="customize-profile-page"),
    path('get-premium/', views.get_premium, name="get-premium-page"),
    path('try-premium/', views.try_premium, name="try-premium-page"),
    path('activate/<slug:uidb64>/<slug:token>)/', views.activate, name='activate'),
    # 4 built-in views for password reset:
    # - password_reset sends the mail
    # - password_reset_done shows a success message for the above
    # - password_reset_confirm checks the link the user clicked and prompts for a new password
    # - password_reset_complete shows a success message for the above
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            form_class=EmailValidationOnForgotPassword,
            subject_template_name='users/password_reset_subject'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
