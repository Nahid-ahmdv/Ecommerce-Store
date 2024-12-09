from django.urls import include, path

from . import views

app_name = "checkout" #using 'app_name' makes it easier for us to access the urls from our template.

urlpatterns = [
    path("deliverychoices", views.deliverychoices, name="deliverychoices"),
    path("basket_update_delivery/", views.basket_update_delivery, name="basket_update_delivery"), #This path is gonna pass over the AJAX request (information) to a new view called ‘basket_update_delivery’.
    path("delivery_address/", views.delivery_address, name="delivery_address"),
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    # path('request/', views.send_request, name='request'),
    # path('verify/', views.verify , name='verify'),
    path("payment_complete/", views.payment_complete, name="payment_complete"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
]