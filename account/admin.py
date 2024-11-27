from django.contrib import admin
from .models import UserBase
# Register your models here.

#we want to register our custom user model called 'UserBase', so it appears on the admin area.
admin.site.register(UserBase)