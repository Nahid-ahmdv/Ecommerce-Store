from django.contrib import admin

# Register your models here.
#for making our models available in the Django admin area and then being able to add some data to them, we need to register them here.

from .models import DeliveryOptions

admin.site.register(DeliveryOptions)