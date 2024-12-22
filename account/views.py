from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
#the two lines below involve functions from Django's utility modules that are used for encoding and decoding data, particularly in the context of handling strings and URLs. 
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from orders.models import Order
# from orders.views import user_orders
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Address, UserBase
from .tokens import account_activation_token
from django.contrib import messages
from store.models import Product
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
            # return HttpResponse('registered succesfully and activation sent') #Returns a simple HTTP response indicating that registration was successful and an activation email has been sent.
            return render(request, "account/registration/register_email_confirm.html", {"form": registerForm})
    
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
    orders = user_orders(request)
    return render(request,
                  'account/dashboard/dashboard.html', {orders : 'orders'}
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

# Addresses


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user) #When the user makes a request, we can collect the user id from that request. So when the user’s logged in what they’re going to have is a session in the background. 
    # That session data is potentially going to hold the user id. So here we’re bringing in that request information and we’re collecting the user id from it.
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    #when the user has filled in the form and clicks on the 'Submit' button, they have sent a 'POST' request to this view, so we should capture it with an 'If' statement:
    #if the user has submitted the form:
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST) #we're gonna take the data from the form and put it into this 'address_form' variable.
        if address_form.is_valid(): #that is going to run the data against the database and check to make sure that it is valid (the data types are correct) in order to for the data to be entered into the database. 
            address_form = address_form.save(commit=False)
            address_form.customer = request.user #adding more information to the address_form: we add this field (one of the fields of 'Address' model) manually, so we take that from the request. The request is made by a user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses")) #The 'reverse' function in Django is used to generate URLs from view names.
    #if the user hasn't submitted the form; it is just gonna show them the form:
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
#this time (unlike 'add_address' view) we're taking in the 'id' (address id) as well (which is the name of the parameter 'id' in "addresses/edit/<slug:id>/") so that is the data which is in the url:
def edit_address(request, id): #we're using that 'id' to run against the database to find the data
    #allowing the user to save the updated address in the database:
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user) #get the data from the database
        address_form = UserAddressForm(instance=address, data=request.POST) #get the submitted data
        #we now know what address we want to edit because we collected the data from the database, we have got the 'instance' (old data) and 'data' (new data). now we want to apply that new data so we use (address_form.save()).
        if address_form.is_valid():
            address_form.save() #the address has been updated in the database.
            return HttpResponseRedirect(reverse("account:addresses"))
        
    #if we're not saving the data we just want to display the data: 
    else:
        address = Address.objects.get(pk=id, customer=request.user) #Despite getting the 'id' of the address, we also get the customer (id) so that every user can access their own addresses but not those of others. For example, a user cannot enter a random string and gain access to another user's address. finally what gets displayed on the form is the address that got returned (the data about the address that's returned from the database).
        address_form = UserAddressForm(instance=address) #we're getting the form and injecting that data within 'address' variable
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id): #we're gonna take in the address id so we can run against the database to delete it, so we know which address we're going to delete.
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


#we want to allow the user to set a default address so that it just automaically appears when they go to purchase something 
@login_required
#What we want to do here is we want to set it so that if we come from the page where we click the button instead of 
# the normal dashboard view we want to capture the fact we’ve come from that page and then send them back to that page 
# when they press the button instead of redirecting them to “account :addresses”. We’re just going to setup a redirect based upon where the person has come from. 
# For this purpose we’re gonna collect the previous url
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
     
    #set up a redirect based upon where the person has come from:
    previous_url = request.META.get("HTTP_REFERER") #This is gonna be the link back to the page we’re on currently. This is the address of where the user came from to get to this page. We’re gonna look inside of that if the word “delivery_address” is in it we redirect the user back that page (back to (“checkout:delivery_address”))

    if "delivery_address/" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("account:addresses")


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})

# @login_required
# def user_latest_order(request):
#     # Get the latest order for the logged-in user
#     latest_order = Order.objects.filter(user=request.user).order_by('-created').first()  # Get the most recent order

#     return render(request, 'checkout/payment_successful.html', {'latest_order': latest_order})

@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})


@login_required #This decorator ensures that only authenticated users can access this view. If a user is not logged in and tries to access this view, they will be redirected to the login page.
def add_to_wishlist(request, id):
    #grab (collect) the item (prouct) (from the database):
    product = get_object_or_404(Product, id=id) #This line retrieves a specific 'Product' instance from the database based on the provided 'id'. If the product does not exist, it raises a 404 error.
    if product.users_wishlist.filter(id=request.user.id).exists(): #This checks if the currently logged-in user (identified by 'request.user.id') already has the specified product in their wishlist by querying the 'users_wishlist' ManyToManyField.
        #when a user sends an HTTP request to the server, their session data is also sent along with that request. In Django, both the HTTP request and the session data are encapsulated in the request object that is passed to your view functions.
        
        product.users_wishlist.remove(request.user) 
        messages.success(request, product.title + " has been removed from your WishList")
        #If the user already has the product in their wishlist, it removes them from the 'users_wishlist' and sends a success message indicating that the product has been removed.
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your WishList")
        #If the user does not have the product in their wishlist, it adds them to the users_wishlist and sends a success message indicating that the product has been added.
    return HttpResponseRedirect(request.META["HTTP_REFERER"]) #Finally, it redirects the user back to the page they came from using 'HTTP_REFERER', which contains the URL of the previous page.
'''
Role of ManyToManyField:
In this context, users_wishlist is defined as a ManyToManyField in your Product model:

python
users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

Purpose: This field allows multiple users to save multiple products in their wishlists. 
Each user can have several products in their wishlist, and each product can be saved by multiple users.
Intermediary Table: Django automatically creates an intermediary table to manage this relationship, 
allowing efficient querying and management of which users have which products in their wishlists.
'''

'''
when a user sends an HTTP request to the server, their session data is also sent along with that request. In Django, both the HTTP request and the session data are encapsulated in the request object that is passed to your view functions.
Breakdown of the Concept
1)HTTP Request:
    . When a user interacts with a web application (e.g., by clicking a link or submitting a form), their browser sends an HTTP request to the server. This request contains various information such as:
        . Request method (GET, POST, etc.)
        . URL being requested
        . Headers (including cookies)
        . Any data submitted with the request (e.g., form data)
2)Session Data:
    . Django uses sessions to store information about the user across requests. This session data can include user-specific information like authentication status, user preferences, and other temporary data.
    . The session data is typically stored on the server and is associated with a unique session ID that is sent to the client as a cookie.
3)The request Object:
    . In Django views, the request object provides access to both the HTTP request data and the session data. You can access session data through request.session.
    For example:
python
def my_view(request):
    # Accessing session data
    user_id = request.session.get('user_id')
    # Accessing other request data
    if request.method == 'POST':
        form_data = request.POST
Summary
In summary, when you refer to "request" in Django, it encompasses both the HTTP request sent by the user and any associated session data. This allows you to handle user interactions and maintain state across different requests effectively. 
'''