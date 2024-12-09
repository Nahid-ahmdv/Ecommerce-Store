from django.contrib import admin

# Register your models here.


from .models import Order, OrderItem

# admin.site.register(Order)
# admin.site.register(OrderItem)
# from django.contrib import admin
# from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'order_key', 'total_paid', 'created')  # Add order_key here
    fields = ('user', 'full_name', 'email', 'address1', 'address2', 'city', 
              'phone', 'postal_code', 'country_code', 'total_paid', 
              'payment_option', 'billing_status')  # Include order_key here

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)