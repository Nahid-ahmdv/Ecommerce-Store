from django import forms #by this we brought in 'forms' module from Django framework.
from store.models import Product, Category #by this we can grap the data from 'Product' table.

# ارث‌بری می‌کنیمforms.Form ارث‌بری کنیم و در کلاس متا هم اسم آن مدلی که قرار است فرم را براساسش بسازیم، می‌نویسیم. در مقابل اما اگر فرم‌مان مستقل است از forms.ModelForm اگه فرمی که می‌خواهیم بسازیم وابسته به مدل خاصی باشد، باید از 
#'forms.ModelForm': Directly tied to a specific model. You specify which model to use in the Meta class, and it automatically generates fields based on that model.
#'forms.Form': Does not have any direct association with a model. You define all fields manually, and it can be used for various purposes (e.g., search forms, login forms).
#let's go ahead and create a new form for our search.
class ProductSearchForm(forms.Form):
    h = forms.CharField()  #we're not gonna build a form, we're gonna utilize Django and tell Django what type of form we want and we do that by basically set  up this variable 'q'('h') (query).Basically we're gonna say from 'forms' we just want to build a character field input. we just told Django that we want to make a new form and we want one input and that's just gonna be a character field. (ساختیم product_search و ویوای به نام views.py رفتیم توی فایل)
    cgry = forms.ModelChoiceField(queryset=Category.objects.exclude(name='default').order_by('name'))#next up we want to add the drop-down facility so not only do we want the user to be able to search for a word, we want to be able to let them select a category we want to search within. 'ModelChoiceField' is gonna create a drop-down choice field.

    #The __init__ method in a Django form is used to customize the form's initialization process. This defines the constructor for the form class. It allows you to pass additional arguments and keyword arguments when creating an instance of the form.
    def __init__(self, *args, **kwargs): #we're gonna return some arguments back
        super().__init__(*args, **kwargs) #This calls the parent class's (forms.Form) constructor, ensuring that any initialization defined in the parent class is also executed. This is essential for maintaining proper functionality.
        self.fields['cgry'].required = False #we're gonna select the field 'cgry' and put it as unrequired

        self.fields['cgry'].label = 'Category' #This sets a custom label for the cgry field that will be displayed in the form.
        self.fields['h'].label = 'Search For' #Similar to the previous line, this sets a custom label for the search input field h, changing its label to "Search For".

        self.fields['h'].widget.attrs.update(
            {'class': 'form-control menudd'})
        self.fields['h'].widget.attrs.update( #This line adds a data attribute called data-toggle, which is commonly used with Bootstrap to enable dropdown functionality when interacting with elements. It indicates that this input field can trigger a dropdown menu.
            {'data-toggle': 'dropdown'})
        #Field Definitions:
            # h: A character field for entering the search term.
            # cgry: A dropdown field for selecting a category, which excludes any category named "default".