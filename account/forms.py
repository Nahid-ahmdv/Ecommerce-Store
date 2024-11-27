from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from .models import UserBase


#our customized login form:
class UserLoginForm(AuthenticationForm): #we're not actually building the form here, we're just overriding this.
    #widgets are gonna inject into the input areas of all the instance forms of this class.
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'})) #more about 'id' in the WordPad #The id attribute provides a unique identifier for each form field in the HTML output. This is particularly useful when you need to reference specific elements in JavaScript or CSS.
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


#using a form to add instances to your UserBase model:
#we're gonna use the form below to add instances to our 'UserBase' model.
'''
Using a form is essential for adding instances to your 'UserBase' model as it provides validation, convenience, error handling, and security. 
By creating a 'ModelForm', you can streamline the process of gathering user input and ensuring that it adheres to your model's requirements. 
'''
class RegistrationForm(forms.ModelForm):#This class is defined as a subclass of 'forms.ModelForm' (is extended from 'ModelForm'), which means it is directly tied to a Django model—in this case, the 'UserBase' model.
#In the Meta class of the form, we specify that the model to be used is 'UserBase' and define which fields from that model should be included in the form.
#This means that when you create an instance of 'RegistrationForm', it will automatically handle validation and data binding for the specified fields ('user_name' and 'email') based on the 'UserBase' model.
    
  #our form is simple and we're not gonna use all the fields we've set out in our 'UserBase' modelو but just the two of them.
    #we need to make sure that the form inputs, we're creating here, match up with the data fields that exist in our 'UserBase' model, otherwise this isn't going to work.
    user_name = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required') #'models.CharField' is used for defining character fields in your database schema with constraints like maximum length (it represents a column in the database table.), while 'forms.CharField' is used for creating form fields that handle user input and validation.
    email = forms.EmailField(label='Email address', max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput) #The 'PasswordInput' widget is specifically designed for password fields. It renders an HTML <input> element of type 'password', which masks the characters entered by the user. This is important for security, as it prevents others from seeing the password as it is typed.
    #A widget is Django's representation of an HTML input element. The widget handles the rendering of the HTML, and the extraction of data from a GET/POST dictionary that corresponds to the widget.
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    
    #The 'Meta' class allows you to specify which model the form is associated with:
    class Meta:
        model = UserBase #This line indicates that the 'RegistrationForm' is linked to the 'UserBase' model, meaning that the form will be used to create or update instances of this model.
        fields = ('user_name', 'email',) #The 'fields' attribute within the 'Meta' class specifies which fields from the model should be included in the form. This means that only the 'user_name' and 'email' fields from the 'UserBase' model will be included in the form. 
    
    #adding some different validation checks (we can do this (adding the following checks) on the view or model, but we're just doing it here.):
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower() #checking the user_name against the database.
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists!")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match!')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email'] 
        if UserBase.objects.filter(email=email).exists(): #checking the email against the database.
            raise forms.ValidationError(
                'Please use another Email, that is already taken!')
        return email

#For managing the styling of the inputs of our registration form, we can’t actually add anything into the inputs within the register page (register.html) because in 
# register.html we’re just asking Django to output the input elements (form fields) on the page via for example {{ form.user_name }}, so what we can do here is we can access these fields 
# through super() and then through widgets we can update and include some information. So this code snippet here is allowing us to access the individual input items to add some additional data and styling to it (some additional context).
#(more description about the following code snippet on the WordPad file.)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
'''
In summary, overriding the '__init__' method in a Django form allows you to customize how form fields are initialized and styled. 
The call to 'super().__init__(*args, **kwargs)' ensures that all necessary initialization from the parent class occurs before applying your customizations. 
This practice helps maintain proper functionality while allowing for flexibility in how forms are presented in your application.
'''


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Account email (can not be changed)', 
        max_length=200, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3', 
                'placeholder': 'email', 
                'id': 'form-email', 
                'readonly': 'readonly', #Here I’m adding ‘readonly’ because I don’t want them to be able to update their email.
                'autocomplete': 'email'
            }
        )
    )

    first_name = forms.CharField(
        label='Firstname', 
        min_length=4, 
        max_length=50, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3', 
                'placeholder': 'Firstname', 
                'id': 'form-firstname', 
                'autocomplete': 'given-name'  # Use appropriate autocomplete value
            }
        )
    )

    class Meta:
        model = UserBase  # Ensure this is your actual user model
        fields = ('email', 'first_name')

    #That’s just again some validation checking to make sure that the user has entered everything where they need to enter the data.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True #because of 'readonly' we won't to be able to type anything there.


class PwdResetForm(PasswordResetForm):

    #we have got just one input for the password reset form and that is the email. The user has to type in their email address of the account that they have, and then we're gonna send an email to that account
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email'] #just to make sure it is in the right format for an email
        u = UserBase.objects.filter(email=email) #we go over to the UserBase and then select where the email equals email, now we have got the user.
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email
    
    
class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))