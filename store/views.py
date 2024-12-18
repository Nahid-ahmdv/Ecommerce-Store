#This is where l start to connect everything up now in my project.
from django.shortcuts import (  # If data doesn't get retrieved, we're gonna return a 404.
    get_object_or_404, render)

from .models import (  # I'm working with models so I need to bring the models in so I have access to them.
    Category, Product)


# Create your views here.
#HomePage:
def product_all(request): #request: This is the user's request information
    # products = Product.objects.filter(is_active = True) #This line made sure that any product that was selected as active was showen on our storefront. instead of this line we can make a custom manager and write the below line.
    products = Product.products.all()#This returns a QuerySet containing all instances of the 'Product' model with 'is_active = True'. (this is running some queries on the 'Product' table and collecting all the data). #first we need to grab the data that we're gonna want to show on the HomePage. 
    #A QuerySet is essentially a collection of database queries that represent a set of objects from your database. It allows you to retrieve, filter, and manipulate data stored in your database models.
    return render(request, 'store/home.html', {'products': products}) #I'm trying to build a HomePage which has all the data from my database (all the products that is in my store).
    #In Django 'render' is used for loading the templates.
    #'store/home.html': It's a template shortcut
    #by 'return render(..)' we're basically telling Django to get the data ({'products': products}), get the template ('store/home.html'), prepare the template with the data and then send it back to the user.
    #We should tell Django where our templates are stored, we do that by adding ''DIRS': [BASE_DIR / 'templates'],' to the TEMPLATES in settings.py, now Django looks for a folder named 'templates' in the project's root directory to find templates.

'''the below view was just to drop-dow 'categories' list in the navbar, we remove it and rewite it on the 'context_processors.py' file'''
# def categories(request):
#     return {
#         'categories': Category.objects.all() #we're gonna collect all the categories in 'Category' table.
#     }

def product_detail(request, slug): ##this value here 'slug' represents that value on 'urls.py' file (that left 'slug' in '<slug:slug>/'). so now what we're going to do is utilizing this information to make a query to the database. so in SQL terms the query that we're going to make is select all from 'Product' model (table) where slug is equal to whatever is in here ('slug'). (but first we import "get_object_or_404" which is going to be utilized if the object doesn't exist the webpage is going to return 404).
    product = get_object_or_404(Product, slug=slug, in_stock=True) #this query stores that individual product into variable 'product' and then by next line we pass it over to our template 'detail.html' #select from the database 'Product', where slug equals slug and is in stock.
    return render(request, 'store/products/singleproduct.html', {'product': product}) #We need to stick the data into the template and then return the prepared template. so now we should build this 'detail.html' page.

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug) #making query on the 'Category' database.finding and selecting one object in the 'Category' database where the slug field equals to 'category_slug'.That's gonna return one object from the database.
    products = Product.products.filter(category=category) #making query on the 'Product' database. and that's gonna return a list of products.
    return render(request, 'store/products/category.html', {'category': category, 'products': products})