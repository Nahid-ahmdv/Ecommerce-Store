from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
#the two lines below involve functions from Django's utility modules that are used for encoding and decoding data, particularly in the context of handling strings and URLs. 
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# from orders.views import user_orders
from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .tokens import account_activation_token
from django.contrib import messages
# Create your views here.

#When a user fills out a registration form and clicks submit button, the data is sent as part of an HTTP request to the server, 
# and more accurate to a specific URL that maps to the 'account_register' view function in your Django application. The view processes this request, including any form data submitted by the user.
def account_register(request):

    if request.user.is_authenticated: #first of all we need to check to see if the user is authenticated and logged in, if this is the case, we should return\redirect them somewhere. 
        # return redirect('account:dashboard')
        return redirect('/') #This prevents logged-in users from accessing the registration page again.
    

    # now we need to collect the information. just remember, this view is gonna be utilized when the user presses that 'register' or 'submit' button. All that form data is gonna be sent off to the specific URL which is going to then be pointed to this view and we're gonna do something with it.
    ##Handle GET Request:
    if request.method == 'POST': #This checks if the request method is POST, which indicates that the user has submitted the registration form.

        # now we need to collect information from the posted data (user data) and create an instance of 'RegistrationForm' with submitted data (binds the form instance to the data submitted by the user through an HTTP POST request).
        registerForm = RegistrationForm(request.POST) #A new instance of 'RegistrationForm' is created with the data submitted by the user (request.POST). This binds the form to the submitted data for validation.

        # Check if the form is valid:
        if registerForm.is_valid(): #This checks if the form data is valid according to the rules defined in the 'RegistrationForm'. If valid, it proceeds to create a new user account.

            # Process valid data (e.g., create a new user)
            user = registerForm.save(commit=False) #this line creates a new user instance but does not save it to the database yet. This allows you to modify fields before saving.
            
            #After calling 'is_valid()', you can safely access user input through 'cleaned_data'. This dictionary contains only those fields that passed validation.
            user.email = registerForm.cleaned_data['email'] #This line sets the user's email address from the cleaned data of the form.
            user.set_password(registerForm.cleaned_data['password']) #Hashes and sets the user's password securely.
            user.is_active = False #Sets 'is_active' to False, indicating that the account needs to be activated (likely via email).
            user.save() #Saves the user instance to the database.


            #Prepare Activation Email:
            current_site = get_current_site(request) #Retrieves information about the current site (like its domain).
            subject = 'Activate your Account' #Retrieves information about the current site (like its domain).
            message = render_to_string('account/registration/account_activation_email.html', { #Uses 'render_to_string' to generate an email message using a template (account_activation_email.html). The message includes:
                'user': user, #The user object.
                'domain': current_site.domain, #The domain of the current site.
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),#encoding user id #A URL-safe base64 encoded version of the user's primary key (uid which stands for user ID).
                'token': account_activation_token.make_token(user), #An activation token generated for this user.
            })

            #Send Activation Email:
            user.email_user(subject=subject, message=message) #Sends an email to the newly registered user with instructions on how to activate their account using the generated subject and message.
            
            #Response After Registration (after the email is sent):
            return HttpResponse('registered succesfully and activation sent') #Returns a simple HTTP response indicating that registration was successful and an activation email has been sent.
    
    
    #Handle GET Request:
    else:
        registerForm = RegistrationForm() #If the request method is not POST (i.e., it's a GET request), it creates an empty instance of 'RegistrationForm'. This will be used to render the registration page for users who are visiting it for the first time.
    return render(request, 'account/registration/register.html', {'form': registerForm}) #Renders the registration template (register.html) with the form context so that users can fill it out.
'''
summary
The 'account_register' function handles user registration by checking if a user is already authenticated, processing form submissions, validating input data, creating a new user account, sending an activation email, and rendering the registration form for GET requests. 
This flow ensures that users can register securely while also requiring them to activate their accounts via email verification.
'''

#Once the user clicks the link, you can extract the uidb64 and the token from the URL via the following view and use them to verify if it is valid by calling check_token(user, token). If valid, you can proceed to activate their account.
def account_activate(request, uidb64, token): #remember that in our url (path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),) we're passing two parameters (uidb64' and 'token') across so we're gonna need to pass those across as well as the 'request'.
    try: #First try and get the data (collecting the data that has been passed through):
        uid = force_str(urlsafe_base64_decode(uidb64)) #decoding hashed user id
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save() #because we've changed the status of 'is_active' field, we should save the user data again to update it.
        login(request, user) #after updating the user data, now we're gonna logged them in, and then we're gonna redirect them to the dashboard.
        return redirect('account:dashboard') #we've also already set out a redirect path in the core/settings.py 'LOGIN_REDIRECT_URL = '/account/dashboard''
    else:
        return render(request, 'account/registration/activation_invalid.html')
    
'''
urlsafe_base64_decode(uidb64):
    This function is used to decode a URL-safe base64 encoded string. In the context of Django, this is often used for decoding user IDs that have been safely encoded for inclusion in URLs (e.g., during account activation or password reset processes).
    'uidb64' is expected to be a base64 encoded string representing the user’s primary key (ID).
force_text(...):
    The 'force_text' function is used to ensure that the output from 'urlsafe_base64_decode' is converted to a string (text). In Django 3.0 and later, 'force_text' has been replaced with 'force_str', which is preferred for converting bytes to strings in a more consistent way across Python versions.
    If you are using Django 3.0 or later, you should use force_str instead of force_text.
'''


@login_required #that is gonna check the user is logged in or not, and then if they're logged in it's gonna allow them access to this (dashboard) page.
def dashboard(request):
    return render(request,
                  'account/dashboard/dashboard.html',
                )


@login_required #only authenticated users can access this view. If a user who is not logged in tries to access this view, they will be redirected to the login page.
def edit_details(request): #This function (view) is designed to handle the editing of user details.
    #The function 'edit_details' takes a single parameter, 'request', which contains all the information about the HTTP request made by the client (browser).
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST) 
        #If it’s a POST request, a new instance of 'UserEditForm' is created with two arguments:
            #instance=request.user: This populates the form with the current user's existing data, allowing them to edit their details.
            #data=request.POST: This contains the data submitted through the form.

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Details successfully updated!")  # Optional: add success message
            return redirect('account:dashboard')
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/dashboard/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user) #we get the user id via 'request.user'.
    user.is_active = False #We’re not actually going to delete the user’s account, we’re just gonna flag their account to ‘False’ which means they won’t be able to login and then we’re just gonna save the data, and also going to log them out via 'logout(request)'.
    user.save()
    logout(request)
    return redirect('account:delete_confirmation') #so we need another url (endpoint) for 'delete confirmation' page.
