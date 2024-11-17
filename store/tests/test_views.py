from unittest import skip  # This provides us a facility to actually skip tests

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import (  # we want to simulate a user going to our page and accessing our views, etc. we need a tool to do that, so there're two options: first option here is importing 'Client' and that will allow us to kind of simulate a userin a test.
    Client, RequestFactory, TestCase)
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


@skip("demonstrating skipping")
class TestSkip(TestCase):  #by decorating this class with 'skip' and just describing why you're skipping this test (in this case "demonstrating skipping") that allows us to identify tests that have been skipped.
    def test_skip_exmaple(self):
        pass

class TestViewResponses(TestCase):
    #first of all we need to set up the database surely:
    def setUp(self):
        self.c = Client()#we're gonna accesss the client ('Client' instance) as '.c' throughout my tests. #'self.c' is used to create an instance of the 'Client' class, which allows for simulating HTTP requests to the Django application. This is essential for testing how the application responds to various requests without needing to run a live server.
        self.factory = RequestFactory() #RequestFactory: This is used to create mock request objects, which can be useful for testing views directly without going through the full request/response cycle.
        
        
        
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        # Database Setup: The 'setUp' method creates necessary entries in the database for testing:
        #     A user with the username 'admin'.
        #     A category named 'django'.
        #     A product titled 'django beginners', associated with the created category and user.

# Test Methods
# Each method within this class tests a different aspect of the application's functionality.
    '''1)Test Allowed Hosts
            Purpose: This test checks if the application correctly handles requests from allowed and disallowed hosts.
            Assertions:
            A request from a disallowed host (e.g., 'noaddress.com') should return a status code of 400 (Bad Request).
            A request from an allowed host (e.g., 'yourdomain.com') should return a status code of 200 (OK).'''

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com') #when we make a GET request to this page (Homepage) what's gonna return from the server is the status code (HTTP response status code). 200 means we've retrieved the data and everything is OK, the page has returned correctly. 
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com') #because of the changes that I made on 'settings.py' file in 'ALLOWED_HOSTES', this domain should work when I try and access the website.
        self.assertEqual(response.status_code, 200)


    '''
        2) Test Homepage URL
            Purpose: This test checks if the homepage URL responds correctly.
            Assertion: The homepage should return a status code of 200, indicating that it is accessible.'''
    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/') #we've used the client to send a HTTP response GET request to this path. #The Client instance (self.c) is utilized throughout the test methods to make GET or POST requests to different URLs defined in the application. For example: This line sends a GET request to the homepage ('/') and stores the response in the variable 'response'.
        self.assertEqual(response.status_code, 200)



    '''
        3) Test Product List URL
            Purpose: This test checks if the category list page for 'django' responds correctly.
            Assertion: The request to this URL should return a status code of 200.
    '''    
    def test_category_list_url(self):
        """
        Test category response status
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)



    '''
        4) Test Product Detail URL
            Purpose: This test verifies if the product detail page for 'django-beginners' responds correctly.
            Assertion: The request should return a status code of 200.'''
    def test_product_detail_url(self):
        """
        Test products response status
        """
        response = self.c.get(
            reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    
    
    '''
        5. Test Homepage HTML Content
            Purpose: This test checks that the HTML content returned by the homepage contains specific elements.
            Assertions:
            The HTML should include <title>HomePage</title>.
            The HTML should start with a valid doctype declaration.
            The response status should be 200.
    '''
    #HTML validation test
    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()#we want to simulate a request directly to the 'product_all' view not through the corresponding URL.  #This line creates a new instance of 'HttpRequest'. This object simulates an HTTP request that can be passed to the view function being tested (in this case 'product_all').
        response = product_all(request)
        html = response.content.decode('utf8') #decoding the response
        self.assertIn('<title>HomePage</title>', html)
        self.assertTrue(html.startswith('<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)




    '''
        6. Test View Function with Request Factory
            Purpose: This test uses the RequestFactory to create a mock request and tests the view function directly.
            Assertions:
            Similar to the previous test, it checks for specific HTML content and structure.'''
    def test_view_function(self):
        """
        Example: Using request factory
        """
        request = self.factory.get('/products/django-beginners')
        response = product_all(request)
        html = response.content.decode('utf8') #now what we find in this side of this 'html' variable is all the html that's been returned from that page (HomePage in this case).
        self.assertIn('<title>HomePage</title>', html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)


