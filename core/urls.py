"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
# from azbankgateways.urls import az_bank_gateways_urls
# from checkout.bank import go_to_gateway_view, callback_gateway_view

#we use 'namespace' to refer to a view for avoiding hardcoding.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')), #It's better to separate our URLs into the application level.'' is the root directory and the HomePage. and namespace will allow us later on in the program to kind of access our URLs in a more convenient way.
    path('basket/', include('basket.urls', namespace='basket')), #we can't have two pathes starting from the root.
    path('account/', include('account.urls', namespace='account')),
    path('checkout/', include("checkout.urls", namespace="checkout")), #It creates a connection to our checkout/urls.py file.
    path('orders/', include('orders.urls', namespace='orders')),
    # # bankgetways urls
    # path('bankgateways/', az_bank_gateways_urls()),
    # path('go-to-gateway/', go_to_gateway_view, name='go-to-gateway'),
    # path('callback-gateway/', callback_gateway_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#We can either write it like the line below or above.
# if settings.DEBUG:  #while we're working in the development environment (opposite of production environment) we have got "DEBUG = True" and that provides us an additional information when we make mistakes in our project and we can kind of view them in the browser, of course we don't want that to happen in our production environment so we turn that off.
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)