from django.contrib.auth.models import \
    User  # This is the user model that Django automatically builds.
from django.db import models
from django.urls import reverse


# Create your models here.
class ProductManager(models.Manager): #This is a custom manager
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
class Category(models.Model): #we're extending from 'models.Model'. That's gonna provide us access to kind of the functionality that we're gonna need to build and describe a model.
    #things we need to record about a category:
    name = models.CharField(max_length=255, db_index=True) #the datatype of our 'name' field is character field. 'db_index=True' is used to create an index on that field in the database. 
    #Multiple records can share the same value in a non-unique indexed field (like 'name'), but each record will still have a distinct record identified by their unique primary key (ID).
    slug = models.SlugField(max_length=255, unique=True) #In order to get to a specific category we want to type into the browser  '127.0.0.1:8000/the-slug-of-that-category/'.

    class Meta: #data about data. The 'Meta' class is an inner class that provides metadata options for the model. Metadata is anything that’s not a field, such as ordering options, database table names, and human-readable names.
        verbose_name_plural = 'categories' #This attribute in the 'Meta' class of a Django model is primarily used for displaying the plural name of that model in the Django administration interface (admin site) and other user-facing contexts. This means when you are managing this model in the admin interface, it will show "Categories" instead of a default pluralization "Categorys".
    '''
    While one of the primary uses of the Meta class is to configure how models are displayed in the Django admin area (through options like verbose_name and verbose_name_plural), 
    it also serves many other purposes related to database behavior, relationships, and constraints.
    '''
    
    def get_absolute_url(self): #This method is typically included in a Django model and is used to return the canonical URL for an instance of that model. It allows you to easily retrieve the URL for an object without needing to know its specific path.
        return reverse('store:category_list', args=[self.slug])
    
    '''
    reverse('store:category_list', ...):
      The 'reverse()' function takes the name of the URL pattern as its first argument. In this case, 'store:category_list' refers to a URL pattern defined in your 'urls.py' file under the namespace 'store' named 'category_list'. This pattern should correspond to a view that handles displaying list of categories.
    args=[self.slug]:
      The 'args' parameter is used to pass positional arguments to the URL. Here, 'self.slug' refers to the slug attribute of the model instance (e.g., a unique identifier for the category). This slug will be inserted into the URL where needed, allowing Django to construct the correct path for that specific category.
    example:When you call 'some_category.get_absolute_url()', where 'some_category' is an instance of 'Category' model, it will return a URL like '/store/my-first-category/', assuming the slug for that category is 'my-first-category'.'''
    def __str__(self): #dunder string method
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE) #by defining this foreign key field we build a link between these two tables.
    '''
    class Product(models.Model):
        This line defines a new Django model called 'Product', which inherits from 'models.Model'. This inheritance means that 'Product' will have all the functionalities provided by Django’s ORM (Object-Relational Mapping) system, allowing you to interact with the database easily.
    category = models.ForeignKey(...):
        The category field is defined as a foreign key. A foreign key is a field that creates a many-to-one relationship between two models. In this case, each product can be associated with one category, but each category can have multiple products.
        The foreign key points to the 'Category' model, indicating that each product is linked to a specific category.
    Parameters of ForeignKey:
        Category: This specifies the model that the foreign key points to. In this case, it references the 'Category' model.
        related_name='product': This parameter defines the name of the reverse relation from the 'Category' model back to the 'Product'. When you access a category instance, you can use this related name to get all products associated with that category.
        For example, if you have a category instance called 'electronics', you can retrieve all products in that category using:
        python
        electronics.product.all()
    on_delete=models.CASCADE: This parameter specifies what should happen when the referenced category is deleted. The CASCADE option means that if a category is deleted, all associated products will also be deleted automatically. This helps maintain referential integrity in your database by ensuring there are no orphaned product records.
    '''
    created_by = models.ForeignKey(User, related_name='product_creator', on_delete=models.CASCADE, default='admin') #I want to record who actually made that data so I made a foreign key to the Django default 'User' table. so we need to add 'User' table into our database, so we need to import that model in (line 2).
    title = models.CharField(max_length=255) #The title of the product.
    author = models.CharField(max_length=255, default='admin') #The author of the book.
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/') #(we should have Pillow (which is a package that helps us manage images) installed) I'm gonna assume that the product only has one image. we're not actually storing the image in the database; we're storing the link of the image to the database. So we're gonna have to set up that link system (steps 2 and 3 below).
    #we just have to create a new folder called 'media' in the main root of our project. we don't need to also create 'images' folder inside of this 'media' folder, this is just gonna create automatically and Django is gonna do that for us.
    '''
    image:
        This is the name of the field in the model. It will be used to reference the uploaded image in instances of this model.
    models.ImageField:
        ImageField is a specialized field type in Django that inherits from FileField. It is specifically intended for storing image files. When you use ImageField, Django performs checks to ensure that the uploaded file is a valid image format (e.g., JPEG, PNG, GIF).
    upload_to='images/':
        The 'upload_to' parameter specifies the directory within your media root where uploaded images will be stored. In this case, images will be saved in a folder named 'images/' in your media root.
        This path is relative to the 'MEDIA_ROOT' setting in your Django project, which defines the base directory for media files.
    How It Works
     When a user uploads an image through a form that uses this model, Django handles the file upload process as follows:
       Storage: The uploaded image file is saved to the specified directory (images/) under the 'MEDIA_ROOT'.
       Database Entry: The path to the uploaded image file is stored in the database, allowing you to retrieve it later.
       Validation: Django uses the Pillow library (which must be installed) to validate that the uploaded file is indeed an image and can also handle various image processing tasks.
    Additional Considerations
    1)Pillow Library: To use ImageField, you need to have the Pillow library installed.
    2)MEDIA_URL and MEDIA_ROOT:You should configure your settings.py to define 'MEDIA_URL' and 'MEDIA_ROOT'. For example:
            MEDIA_URL = '/media/'
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
            This configuration allows Django to serve media files during development.
    3)Serving Media Files:In development, you can serve media files using Django's built-in server by adding URL patterns in your urls.py:
            from django.conf import settings
            from django.conf.urls.static import static
  
            urlpatterns = [
                # Your other URL patterns
            ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    4)Accessing Uploaded Images:In templates, you can access the uploaded image URL like this:
            xml
            <img src="{{ instance.image.url }}" alt="Product Image">
            Here, instance refers to an instance of your model that contains the uploaded image.
    For example, if you set:
    python
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    And you have an image uploaded to 'images/', the actual file path on your server would be something like:
    text
    /path/to/your/project/media/images/your_image.jpg
    '''
    slug = models.SlugField(max_length=255) #In order to get to a specific product we want to type into the browser '127.0.0.1:8000/the-slug-of-that-product/'.
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True) #There might be some products that aren't actually active to buy, maybe for example you've run out of stock.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager() #default manager
    products = ProductManager() #custom manager
    '''
    If you set 'auto_now=True', every time you save an instance of that model, the timestamp will update.
    If you set 'auto_now_add=True', it will only set the timestamp once at creation, and any subsequent saves will not affect this field.
    '''
    class Meta:
        verbose_name_plural = 'Products' #unnecessary
        ordering = ('-created_at',)  #when we return all the data from 'Product' table we can specify what order we want that data to be in. Here we're ordering our list that gets returned from the database in descending order. It means that for example the last item that is added to the database is shown first.

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug]) #the name 'store' is the app_name we wrote in urls.py file for a quick reference point to the 'urlpatterns' we wrote there, and 'product_detail' is the actual url name path, so 'store:product_detail' is the url that we want to use.

    def __str__(self):
        return self.title