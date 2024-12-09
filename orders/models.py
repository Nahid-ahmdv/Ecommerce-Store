import uuid
from django.db import models
from decimal import Decimal
from django.conf import settings #we're gonna need the settings to access the user table (UserBase).
from django.db import models
from store.models import Product

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user") #'user' field is connected to the user model (AUTH_USER_MODEL = 'account.UserBase'), so we can collect what user has made the order (payment).
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100) 
    phone = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID field
    payment_option = models.CharField(max_length=200, blank=True)
    billing_status = models.BooleanField(default=False)

    class Meta:
        #In Django, the 'ordering' option within the 'Meta' class of a model specifies the default order in which query results will be returned when you retrieve instances of that model from the database.
        ordering = ('-created',)
        '''
        Ordering Field:
            The field specified in the 'ordering' tuple is 'created', which is a 'DateTimeField' that records when each order instance was created.
        Descending Order:
            The hyphen (-) before 'created' indicates that the ordering should be in descending order. 
            This means that when you query for orders, they will be returned starting with the most recently created order first.
        '''
    def __str__(self):
        return str(self.created)

#for each order there's multiple items so we have got a one-to-many relationship (A foreign key creates a many-to-one relationship from the child table (OrderItem) to the parent table (Order). This means multiple records in the child table can reference a single record in the parent table.)
class OrderItem(models.Model):
    #we're gonna have a foreign key to the 'Order' and 'Product' table:
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE) #This means that each 'OrderItem' instance is associated with one 'Order' instance.
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE) #This means that each OrderItem instance is associated with one 'Product' instance.
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)