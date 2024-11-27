from django.contrib.auth import views as auth_views #the pre-built views for the authentication processes (like Login\Logout processes). we're gonna hook into that and override some of the settings. we can do this in the 'views.py' but we're just gonna lay all this out in the urls.py.
from django.urls import path
from . import views
from django.views.generic import TemplateView
from .forms import (PwdResetConfirmForm, PwdResetForm, UserLoginForm)


app_name = 'account' #it should be the same as 'namespace' in 'path('account/', include('account.urls', namespace='account')),' that we wrote in core/urls.py. It makes it much easier for us to call our urls in our templates for example.

urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'), #according to the url in 'account_activation_email.html' we have got the 'uid' (user id) and the 'token'. so there are two things here that we're passing in to our url and we're trying to capture those. 
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'), #This new path called 'dashboard' is gonna connect to views.dashboard
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'), #when a user logs out, the next page, where the user is gonna be taken to, is the login page.
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/dashboard/delete_confirm.html"), name='delete_confirmation'),
    # Reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/password_reset/password_reset_form.html",
                                                                 success_url='password_reset_email_confirm', #to tell the user that "if you can check your email you'll then be able to reset your password".
                                                                 email_template_name='account/password_reset/password_reset_email.html', 
                                                                 form_class=PwdResetForm), name='pwdreset'),

    #'password_reset_confirm/<uidb64>/<token>': This is the format similar to what we’ve done previously when we activated the account so we need to take in these parameters (uidb64) and (token) so that we can verify the user when they click on the link that has been sent to their email.
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset/password_reset_confirm.html',
                                                                                                success_url='/account/password_reset_complete/', 
                                                                                                form_class=PwdResetConfirmForm,), name="password_reset_confirm"),
    #by paying attention to the last two pathes, you will realize that in the first path, we start our 'success_url' with no '/' but in the second path we do. 
    # having a '/' at the start means that we want to continue the url that we're currently using. but when we use '/' it is referring to the root directory. 
    # so in the first path we redirect to 'http://127.0.0.1:8000/account/password_reset/password_reset_email_confirm/' as the success url, but in the second one we redirect to 'http://127.0.0.1:8000/account/password_reset_complete/'as the success url.
    
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/password_reset/reset_status.html"), name='password_reset_done'), #for showing 'Password Reset Success Check your email for instructions'.
    path('password_reset_complete/',
         TemplateView.as_view(template_name="account/password_reset/reset_status.html"), name='password_reset_complete'), #for showing 'Password Reset Completed! login'
]