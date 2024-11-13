from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


#when we run tests, we run tests on a separate database; so we've made a database already (.coverage) we don't run tests on our production (main) database.
class TestCategoriesModel(TestCase): #This class will contain tests related to the 'Category' model.

    def setUp(self): #It's a stage in the testing that you create your data which you want to test against.
        self.data1 = Category.objects.create(name='django', slug='django') #The default object manager is 'objects'. we are making an instance in this line. That is gonna go ahead and create an entry into our testing database (.coverage).
        #In order to make the line above available in other methods here, we use 'self' to allow access to this data from other methods throughout our class here for testing.
    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category)) #This line is gonna perform a test.

    def test_category_model_entry(self): #for making a new test we should make a new function. and we already have our data up the top here in the 'setUp' function so we can utilize that again.
        """
        Test Category model return name
        """
        data = self.data1
        self.assertEqual(str(data), 'django') #on the left hand side should match the right hand side. because we've set up that dunder string method in our 'Category' model (__str__), str(data) will return the name of the data which in this case is 'django', and we're gonna test it against 'django' so it should be true.

#we can now do the same thing to our 'Product' model, but for 'Product' model it is a little bit more complicated because it has more fields. 
class TestProductsModel(TestCase): #we create a new class here = a new set of tests.
    def setUp(self):
        Category.objects.create(name='django', slug='django') #remember if we're gonna build a product we're gonna need some categories and a user to actually connect to because we're using them as foreign keys (so we can't build a product without the foreign key dependencies (category and user)).
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                            slug='django-beginners', price='20.00', image='django')
        # self.data2 = Product.products.create(category_id=1, title='django advanced', created_by_id=1,
                                            #  slug='django-advanced', price='20.00', image='django', is_active=False) #why we did use 'category_id' and 'created_by_id' instead of 'category' and 'created_by'? 'cause if you check out the 'Product' table in the 'db.sqlite3' database, you can see that there're fields named 'category_id' and 'created_by_id' so for referencing these fields we need to use the same names.
        
    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners') #we test the dunder string method (__str__) to make sure that the default return is the title in this case.