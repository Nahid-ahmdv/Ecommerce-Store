from django.urls import path

from . import views

app_name = 'basket'


# 'basket/' is the prefix (root) for the rest of the urls here:
urlpatterns = [
    path('', views.basket_summary, name='basket_summary'), #the path is the root and then I want to connect this url to a view called 'basket_summary' where we're gonna show all the items in the basket. we can easily access this url through its name 'basket_summary'.
    path('add/', views.basket_add, name='basket_add'), #where we're gonna send the AJAX request created within 'singleproduct.html' off to.
    # path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update'),
]