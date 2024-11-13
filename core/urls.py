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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')), #It's better to separate our URLs into the application level.'' is the root directory and the HomePage. and namespace will allow us later on in the program to kind of access our URLs in a more convenient way.
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#We can either write it like the line below or above.
# if settings.DEBUG:  #while we're working in the development environment (opposite of production environment) we have got "DEBUG = True" and that provides us an additional information when we make mistakes in our project and we can kind of view them in the browser, of course we don't want that to happen in our production environment so we turn that off.
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)