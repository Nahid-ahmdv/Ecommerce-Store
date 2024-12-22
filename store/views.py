#This is where l start to connect everything up now in my project.
from django.shortcuts import (  # If data doesn't get retrieved, we're gonna return a 404.
    get_object_or_404, render)

from .models import (  # I'm working with models so I need to bring the models in so I have access to them.
    Category, Product)

from django.db.models import Q #The Q object allows you to create complex queries by combining multiple conditions using logical operators such as AND, OR, and NOT. This is particularly useful when you need to filter data based on multiple criteria.

from .forms import ProductSearchForm

from django.core import serializers
from django.http import JsonResponse
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


#The 'product_search' view handles both GET and POST requests:
def product_search(request):
    form = ProductSearchForm() #Form Initialization: The view initializes a 'ProductSearchForm' instance.
    h = '' #we created a new variable and it's just empty. we filled it up shortly.
    cgry=''
    results = []
    query = Q()



    # Handle POST request (When a user types into the search box:) for AJAX search suggestions:If the request is a POST (indicating an AJAX call for search suggestions):
    '''
    POST Request: When a user types into the search box:
        1)After typing three characters, an AJAX POST request is sent to your server at '/search/'.
        2)The server processes this request in your Django view (product_search), where it can query 'Product' table based on the search string received.
        3)The server returns matching products as JSON data.
        4)The client-side JavaScript updates the UI with suggestions based on this response.
    '''
    if request.POST.get('action') == 'post': #just checking to see if we're actually receiving an AJAX POST request.

        search_string = str(request.POST.get('ss')) #It retrieves the search string from the input field (with name 'ss'). now we want to do sth with it (perform a query).
        if search_string is not None:
            search_string = Product.objects.filter( #we're gonna query the 'Product' table for titles containing the search string and returns a JSON response with up to 4 results. (we output the data from the database into the variable 'search_string'so now this variable has all the data that's returned from a database). we probably don't want to return hundred items in a drop-down list as a search suggestion. so we can just type in a number here and just limit the amount that gets returned from the database.
                title__contains=search_string)[:4] #we're utilizing JavaScript and Python (of course by default they can't talk to each other so we need to prepare this data so it can be utilized by JavaScript, what we're gonna need to do now is serialize the data that's returned from the database, so we need to import the serializers)
            data = serializers.serialize('json', list(search_string), fields =('id', 'title', 'slug'))  #so we created a new variable called 'data' and we're gonna serialize the data that gets returned from the database (we store the output of the serialization) and we want to serialize in 'json', and then we define what data we want to serialize and what fields we want to get serialized (we probably don't want to return all the data from the database, we're not gonna need the description to be displayed in the drop-down list.)
            #so we just need to return this 'data' to the search page (search.html). so we're gonna return this 'data' in a json response (because we've serialized it as Json in the 'data' ) so we're gonna need to import the 'JsonResponse'.
            return JsonResponse({'search_string': data})   #we're gonna send it back as reference to 'search_string' (that is the reference point to send the data back to, that's how we're gonna collect the data or where it's gonna be stored when we send it back to the search and what we're gonna send back is all the data inside of that(the data that we serialized))
            #است ذخیره میشود json که function در صورت موفقت‌آمیز بودن در ورودی search.html ایی که داریم برمی‌گرداریم به صفحه سرچ‌مان یعنی همانdata دقت کنید این


    # Handle GET request for searching products:If there’s a GET request with a search term (h):
    if 'h' in request.GET: #we're gonna check to see if any data exists in the get request.If the data does exist in the get request (the 'h' data) then we're gonna process this information.
        form = ProductSearchForm(request.GET) #The form is populated with GET data.
        if form.is_valid(): 
            #If the form is valid, it retrieves the cleaned data for both 'h' (search term) and 'cgry' (category).
            h = form.cleaned_data['h'] #once the form has been checked the data is available from the 'cleaned_data'.
            cgry = form.cleaned_data['cgry']  #cgry is gonna hold a value (the id of that category like 1,2,..) it is not gonna hold the category name. now now we need to use this data inside of our query. so we want to query the title contains 'h' and then what we want to do first of all is set up a new filter
            # results = Post.objects.filter(title__contains = h) #now we set up a simple query, we called this 'results' (a variable called 'results') and basically we need to query the 'Post' model and the we say 'objects' and we use a filter. so what we want to filter from the model is to look for all the data where the title contains 'q' (remember 'q' is what someone's typed into the search input).
            #we can use 'contain' assuming that someone's gonna type in single word or words that are grouped together to return the title or the post. Or we can utilize for example 
            #once we start moving to a postgres database we then have more facilities available to make much more complicated search.
            # results = Post.objects.filter(category=cgry).filter(title__contains = h)  #استفاده کنیم cgry این همان کوئری هست که گفتیم باید توش از اطلاعات کپچرشده در
    # return render(request, 'search.html', {'form': form, 'h':h, 'results':results})   #so next up we now have the form, we want to pass that now, we're gonna set up a http response, so we just return the form to the new page that we're gonna build called 'search.html', and then we're gonna send the form data to that template. حالا باید این تمپلیت را بسازیم
            #اگر بخواهیم فیلد مربوط به انتخاب کتگوری را اختیاری کنیم دیگر کوئری ساخته شده در دو خط بالا کار نمیکند به همان دلیلی که در فایل مربوط به فرمز توضیح دادم
            #so we're gonna modulize our query based upon different parameters
            if cgry is not None:
                query &= Q(category=cgry)
            if h is not None:
                query &= Q(title__contains=h)
            results = Product.objects.filter(query)
    return render(request, 'store/search.html', {'form': form, 'h':h,'cgry':cgry, 'results':results})