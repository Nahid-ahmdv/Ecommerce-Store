from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse #to create dynamic links instead of hardcoding them.

from store.models import Category, Product #for adding some data


class TestBasketView(TestCase): #These are tests that are related to testing the view functionality and obviously that's connected to the 'Basket' class.
    #first of all we need to set up the database:
    #We’re gonna make a copy of the User database and also the Product database, 
    # because we need to add some data into that in order for us to when we build the session there’s going to be data. 
    # Because in our ‘Basket’ class we do have a look for the product data and try and extract it from the database, so we’re going to need that database.
    def setUp(self): 
        User.objects.create(username='admin') #adding a new user into the 'User' table.
        Category.objects.create(name='django', slug='django') #To be able to add some products into the 'Product' table, we first need to add some categories into the 'Category' table.
        #making some products:
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        Product.objects.create(category_id=1, title='django intermediate', created_by_id=1,
                               slug='django-intermediate', price='20.00', image='django')
        Product.objects.create(category_id=1, title='django advanced', created_by_id=1,
                               slug='django-advanced', price='20.00', image='django')
        #building some session data (we've added two items to the session data, so that we can perform delete and update test): 
        self.client.post(
            reverse('basket:basket_add'), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True)

    #now we're gonna run some tests (If our program doesn't work, that is not going to work.)
    #first test:
    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary')) #In this case Django is gonna look for the basket urls in the urls.py file where app_name = 'basket' and then look for the 'namespace = 'basket_summary'.
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self): #In the 'add' method within the 'Basket' class we have a 'if/else' statement, so we need to run two tests.
        """
        Test adding items to the basket
        """
        response = self.client.post( #we use it to post some data
            reverse('basket:basket_add'), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True) #according to lines 91,92, and 94 in 'singelproduct.html' we should specify "productid", "productqty", and "action": "post" for adding an item to our basket.
            #XHR: it’s an XML HttpRequest. So when we use Ajax in general terms we’re sending an XML  HttpRequest so we’re just basically telling or setting that up in the request so it can be sent across and we can simulate that action of sending an Ajax request from our frontend.
        
        #So now we’ve sent data to our application so you would imagine at this point our view would handle that information (bring in Basket class, perform the action of adding that to our session) and now we can test to see what is returned.
        #According to our ‘basket_add’ view response, we’ve returned the response of quantity through ’qty’(line 43 in views.py).
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_delete'), {"productid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'baskettotal': '20.00'})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_update'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'baskettotal': '40.00', 'item_total_price': '20.00'})