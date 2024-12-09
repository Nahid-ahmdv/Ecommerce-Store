# Create your models here.
#Just remember that by default the Django framework provides us a user management tool in the admin area and that obviously builds the model for the user and so on.
#That model (Django default User model) really only comes with a few fields and it’s not very useful when we’re trying to build our custom systems like this, because we want to store numerous information about our customers so that kind of forces us to change the User model. 
# That’s a few different ways we can do that in Django. For example, we can go ahead and just extend from the existing (default) Django User model or we can just tell Django we’re gonna use a completely different User model. We chose the second one and now we want to build a custom User model
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin) 
#We are using 'BaseUserManager' to create a custom user manager that overrides the default account management methods, such as those for creating normal users and superusers. By extending from 'AbstractBaseUser', we can define our own User model with custom fields and behaviors, allowing us to customize the authentication process according to our application's specific requirements.
#When we create a new model in Django, we often want it to automatically include default permissions such as add, change, delete, and view. By inheriting from 'PermissionsMixin', our new model gains these built-in permission fields and methods. This mixin provides the necessary functionality to manage user permissions related to that model, allowing us to integrate seamlessly with Django’s permission framework.
import uuid
from django.db import models
from django_countries.fields import CountryField #we used 'pip install django-countries' command and import 'CountryField'.
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


#custom user manager:
#by the class below (custom user manager) we specify the process for creating a superuser and a normal user.
class CustomAccountManager(BaseUserManager): #we need to build our custom user manager. This is going to specify how the user data is saved to the database. what we need to do is build or actually extend from 'BaseUserManager' which is the base user manager in Django (obviously we want to kind of provide some overrides, for example, we're gonna need to sort out the process for creating a superuser and a normal user).
    
    #sorting out the process for creating superusers and normal users:
    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True) #is used to ensure that the is_staff field is set to True for superusers if it hasn't been explicitly provided in the other_fields dictionary. This ensures that all superusers have staff status, which is necessary for them to access the Django admin interface.
        other_fields.setdefault('is_superuser', True) #In our custom User model 'UserBase', we do not need to explicitly define the 'is_superuser' field as a separate boolean field. This is because the 'is_superuser' attribute is a built-in part of Django's 'PermissionsMixin', which you are already inheriting from. The PermissionsMixin provides the necessary fields and methods to manage permissions, including the 'is_superuser' field.
        other_fields.setdefault('is_active', True)
        #Staff: Can access the admin site but requires specific permissions for actions.
        #Superuser: Has unrestricted access and all permissions by default.
        #If you manually create a user and set 'is_superuser=True' without setting 'is_staff=True', that user will not be able to log into the admin interface. This is because Django checks both fields before allowing access.
        #summary: we can't build a superuser unless we set Both 'is_staff' and 'is_superuser' to True.
        '''
        When creating a custom user model in Django, the handling of 'is_staff' and 'is_superuser' fields is crucial for managing user permissions and access to the admin interface.
        In Django's built-in user model, when you create a superuser using the command:
        python manage.py createsuperuser
        Both 'is_staff' and 'is_superuser' are set to True by default. This means that any user created as a superuser will automatically have full access to the Django admin interface and all permissions without needing to specify these fields explicitly.
        When you implement a custom user model, as we've done in our 'CustomAccountManager', you need to explicitly set these fields when creating a superuser.
        '''
        #doing some validations:
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, user_name, password, **other_fields) #when we do build a superuser, we're gonna be asked for the email, user_name, and password. The call to 'self.create_user(...)' executes the logic defined in the 'create_user' method below to create and save a new user instance with the specified attributes.
    '''
    When you call 'create_superuser', it prepares the necessary fields (like setting 'is_staff', 'is_superuser', and 'is_active') and then calls 'self.create_user(...)' to actually create and save the user instance (which in this case, is a superuser).
    '''
    #The method below is responsible for creating and saving a new user instance (both superuser ans normal user) with the provided parameters.
    def create_user(self, email, user_name, password, **other_fields):

        if not email: #we're doing this validation because, the email is what we're using as 'USERNAME_FIELD'.
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save() #for saving the data.
        return user


#custom user model:
class UserBase(AbstractBaseUser, PermissionsMixin): #we're gonna build a completely new User model (table) for saving our users.

    email = models.EmailField(_('email address'), unique=True) #we're gonna define the 'email' field as the actual kind of login unique identifier.
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    # Delivery details
    country = CountryField()
    phone_number = models.CharField(max_length=11, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    # address_line_1 = models.CharField(max_length=150, blank=True)
    # address_line_2 = models.CharField(max_length=150, blank=True)
    # town_city = models.CharField(max_length=150, blank=True)
    # User Status
    is_active = models.BooleanField(default=False) #we want to be able to disable a user instead of deleting their account. When a user sings up, they receive an email. When they click on that email their account will go active and then they can log in. So you can’t actually log in until the account is set to ‘is_active’, so we can use this field as a safeguard and deletion of the account.
    is_staff = models.BooleanField(default=False) #This is a critical part of user management in Django, controlling access to the admin interface. By defaulting to 'False', it ensures that only explicitly designated users can perform administrative tasks, thus enhancing security within your application.
    created = models.DateTimeField(auto_now_add=True) #to record when the account was created.
    updated = models.DateTimeField(auto_now=True) #to record when the account was updated.

    objects = CustomAccountManager() #a custom account manager to save the new user, we need to build it.

    USERNAME_FIELD = 'email' #by this line you are indicating that users will log in using their email addresses instead of a traditional username.
    #In a standard (default) Django user model, the default 'USERNAME_FIELD' is set to 'username'. By changing it to 'email', you can customize the authentication process to use email addresses, which is common in many applications.
    REQUIRED_FIELDS = ['user_name'] #This line defines a list of fields that are required when creating a superuser via the command line or admin interface.

    class Meta:
        verbose_name = "Accounts" #Defines a singular, human-readable name for the model, which enhances clarity in user interfaces.
        verbose_name_plural = "Accounts" #Defines a plural name for the model, ensuring that it is correctly represented when displaying lists of instances.

    def email_user(self, subject, message): #The method 'email_user' in your custom user model is designed to send an email to the user. 
        #self: Refers to the instance of the user model (the user object calling this method).
        #subject: A string representing the subject line of the email.
        #message: The body content of the email.
        send_mail( #The method calls Django's built-in 'send_mail' function to handle the actual sending of the email. This function is part of Django's email handling framework and is commonly used to send emails from Django applications.
            subject, #This is passed directly from the method’s parameter and will be used as the subject line of the email.
            message, #This is also passed from the method’s parameter and contains the content/body of the email.
            'l@1.com', # This is a placeholder for the "from" email address. It should ideally be replaced with a valid sender email address that you control or that your application uses for sending emails.
            [self.email], #This creates a list containing the recipient's email address, which is taken from the instance of the user model (self.email). This means that when you call this method on a user instance, it will send an email to that user's email address.
            fail_silently=False,
        )
        '''
        example:
            user = UserBase.objects.get(email='example@example.com')
            user.email_user('Welcome!', 'Thank you for signing up!')
        '''
    def __str__(self):
        return self.user_name
    
class Address(models.Model):
    """
    Address
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(UserBase, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Address"