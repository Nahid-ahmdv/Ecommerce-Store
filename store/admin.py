#here we just need to tell Django what models we want to use (register them) so that we can start adding data to those models. so we just need to go ahead and describe what we want to include.
from django.contrib import admin
from .models import Category, Product
# Register your models here.

@admin.register(Category) #This decorator is gonna tell Django that we want to register 'Category' model with the Django admin site, linking it to the 'CategoryAdmin' class, allowing it to be managed through the admin interface. in the class below we add some additional information.
class CategoryAdmin(admin.ModelAdmin): #This defines a custom admin class for the 'Category' model, inheriting from 'admin.ModelAdmin'. This allows for customization of how the model is displayed in the admin area.
    #in the following lines I'm gonna tell Django that I want to display things in a very specific way in my admin area:
    list_display = ['name', 'slug', 'get_products']
    prepopulated_fields = {'slug': ('name',)}#پر می‌شود slug وقتی یک کتگوری بخواهیم وارد کنیم، به محض وارد کردن اسمش خودبه‌خود فیلد مربوط به #This attribute allows automatic generation of certain fields based on other fields. Here, it automatically populates the 'slug' field based on the value entered in the 'name' field.
    def get_products(self, obj):
        return obj.product.count()
    get_products.short_description = 'Number of Products'

@admin.register(Product) #This decorator registers the 'Product' model with a custom admin class, 'ProductAdmin', which defines how this model will be displayed and interacted with in the admin panel.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'price',
                    'in_stock', 'created_at', 'updated_at']
    list_filter = ['in_stock', 'is_active'] # This attribute adds filter options on the right side of the list view.
    list_editable = ['price', 'in_stock'] #This attribute allows certain fields to be edited directly in the list view without needing to go into each individual product's detail page. Here, both 'price' and 'in_stock' can be edited inline.
    prepopulated_fields = {'slug': ('title',)}
#Just remember that in admin area I need 'Categories' to be able to add new 'Products'. I'm not allowed to add a product without a category.