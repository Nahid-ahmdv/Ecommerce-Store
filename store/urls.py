from django.urls import path

from . import views

app_name = 'store' #this name should be equal to the namespace in 'core/urls.py'.

#here we need to connect our URLs to the views.
urlpatterns = [
    path('', views.all_products, name='all_products'), #this is the root directory. this view is gonna be all the products (I could just call this HomePage).
    path('products/<slug:slug>/', views.product_detail, name='product_detail'), #we want to connect the URL 'products/<slug:slug>/' to the individual product page so we've connected this URL to the 'product_detail' view.
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
]