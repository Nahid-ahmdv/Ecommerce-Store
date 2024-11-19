#This module is for being able to do CRUD operations on our basket session data (part of the user's session data which is stored uder 'skey' key and we called it user's basket), we're gonna use the methods of 'Basket' class in our views (for handling AJAX requests).
from decimal import Decimal

from store.models import Product


class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """
    #The class below will run once we instantiate this class and then we can access that 'basket' data in last line.
    def __init__(self, request): #This method is typically used to initialize an instance of a class. #when we create a new instance of this class, this function (method) is gonna be initialized and run. Thinking about my session; I want to have it so that when this gets initialized, the kind of session is checked to make sure there’s a session and then if a session doesn’t exist, this session will be created. And what I then want to do is call this potentially on every page the user goes to, so it doesn’t matter what page the user goes to the session will be created and prepared so they can then put any item they want inside of the basket.
        #We gonna use ‘self’ in all of the methods of a class. We’re kind of setting up these functions so that within this class other functions (methods) can access any of the other attributes within these functions.
        #this 'request' is an instance of the 'HTTPrequest' class that the user sends to the server, and inside of it there is lots of different types of data and we want to access that data so that we can check the request and access information within that request to make different decisions and to perform actions. So we’re bringing that into this function here and then what we’re going to do because this is the initialization function we can then make that available within all functions, so we only need to bring this once into this function (__init__).
        '''
        This line defines the '__init__' method, which is the constructor for the class. 
        It takes two parameters: self, which refers to the instance of the class being created, and request, which is expected to be an object that contains session information (typically from a web framework like Django).
        '''
        #Accessing Session Data:
        self.session = request.session #This line assigns the session data from the request object to an instance variable called 'self.session'. This allows the class instance to access session data throughout its methods.
        #'self.session' represents the session object tied to the current user's request.
        #Retrieving Basket Data:
        basket = self.session.get('skey') #Here, it tries to retrieve the value (session data) associated with the key 'skey' from the session. The 'get' method returns 'None' if 'skey' does not exist in the session.
        #you might manage different contexts (like user roles or specific activities) within the same session using different keys or attributes in the session data.
        # For example, in an e-commerce application, you might have a main session for the user and then manage different contexts like A shopping cart (stored under a key like 'cart') (in our case 'skey').
        #Session Keys:Each key in the session dictionary corresponds to a specific piece of data associated with that user's session. You can think of it as having multiple key-value pairs stored in a single dictionary where each key uniquely identifies the data.
        #in Django, a session associated with a user is represented as a dictionary-like object (request.session), where each key refers to specific data stored within that session. 
        if 'skey' not in request.session:
            basket = self.session['skey'] = {} # we need to setup a new session named 'skey' and then we need to define what it equals (we need to define the data within it), so we're gonna use a dictionary.
        self.basket = basket #Finally, this line assigns the value of basket (which is either the existing basket or a new empty dictionary) to an instance variable called 'self.basket' which we just generated. This allows other methods in the class to access and manipulate the basket. (remember that 'basket' is gonna have (part of) the information about the user's session (that part of the information that is stored under the key 'skey')).
        '''
        Both self.session and self.basket are prefixed with self, indicating that they are instance variables. This means each instance of the class will have its own session and basket.
        Single Parameter:
            The constructor '__init__' only takes one parameter, 'request'. This is common in web frameworks (like Django) where the request object contains all necessary information about the current HTTP request, including session data.
            By passing just the 'request', you can access various attributes (like 'session') without needing to pass them as separate parameters (like def __init__(self, request, session):).
            Session Management:
            The line 'self.session = request.session' retrieves the session data from the request object. This allows you to work with session data directly without needing to pass it in as a separate parameter.
            The logic checks for the existence of 'skey' in the session and initializes it if it doesn't exist. This is a common pattern for managing user-specific data (like a shopping cart) in web applications.
            Instance Variable Initialization:
            The instance variable 'self.basket' is set based on the session data. This means that every instance of this class will have its own session and basket, which are initialized based on the current user's request.
        '''
        '''
        Reviewing the whole process again: the user comes to our website now if the user is new (has never been to our website before) then obviously they won’t have a session available, so we need to build a session. Therefore first of all we need to check to see if the user has a session (or not), 
        if the user has a session it means that in their browser they will have a cookie with an id in that cookie and that will be referenced by a session key and that session key is what we’re gonna make up now (self.session.get(‘skey’) : we want to get a session with session key named ‘skey’)
        (‘skey’ is kind of the reference point to utilize, to kind of name this cookie, because we might make many different cookies or sessions, so we can name it ‘skey’.
        '''
    
    #adding new data to our session (that part of the user's session where the session data stored under the key 'skey' and we called it 'basket'):
    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()
    '''
    Structure of the basket:

    basket = {
    'product_id_1': {'price': '10.00', 'qty': 2},
    'product_id_2': {'price': '15.50', 'qty': 1},
    ...
    }

    example:
    basket = {
    '1': {'price': '10.00', 'qty': 2},
    '2': {'price': '15.50', 'qty': 1}
    }
    '''
    #The reason we created the method below is that, in our summary HTML, we implemented a loop that iterates over the user's basket, even though it is not iterable itself. Therefore, we need to create a new feature (the __iter__ method) to make instances of the Basket class iterable, allowing us to loop over the user's basket.
    #the method below allows an object to be iterable. This means that you can use it in a loop (like a for loop) to iterate over its items.
    #it allows instances of the 'Basket' class to be treated like a collection of items, specifically the products in the user's shopping basket.
    ###########When you create an instance of your 'Basket' class and iterate over it, this method is called automatically:(like in 'summary.html')
    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        #Collecting Product IDs:
        product_ids = self.basket.keys() # This line retrieves all the keys from the 'self.basket' dictionary, which represent the product IDs currently stored in the basket.
        '''
            example:
            basket = {
            '1': {'price': '10.00', 'qty': 2},
            '2': {'price': '15.50', 'qty': 1}
            }
            basket.keys() equals to ['1', '2']
        '''
        #Querying Products from Database:
        products = Product.products.filter(id__in=product_ids) #This line queries the database for all products whose IDs are present in the 'product_ids' list. It uses Django's ORM to filter the Product model based on these IDs. The result ('products') is a queryset containing all products that are currently in the user's basket.
        
        #Copying Basket Data:
        basket = self.basket.copy() #This creates a shallow copy of the 'self.basket' dictionary. This is useful because you will be modifying this copy by adding product information without altering the original basket data directly.

        #Associating Products with Basket Items:
        #This loop iterates over each product retrieved from the database. For each product, it adds a reference to that product object into the copied basket dictionary under its respective ID. This allows you to access product details (like name, description, etc.) later when iterating over the basket items.
        for product in products: #'products' is the data coming from the database.
            basket[str(product.id)]['product'] = product #adding additional data to my copied 'basket'.

        
        #Yielding Basket Items:
        for item in basket.values(): #This final loop iterates over all items in the copied basket dictionary. 
            item['price'] = Decimal(item['price']) #It converts the price of each item from a string to a Decimal (to be able to do calculations), ensuring accurate arithmetic operations (important for financial calculations).
            item['total_price'] = item['price'] * item['qty']#adding new 'key:value'to this item which itself is a dictionary. It calculates the total price for each item (subtotal) by multiplying its price by its quantity (item['qty']).
            yield item #The yield statement returns each item one at a time (unlike 'return'), allowing you to iterate over them as if they were elements of a list.
    '''
    Example Usage
    When you create an instance of your 'Basket' class and iterate over it, this method is called automatically:
    python
    basket_instance = Basket(request)

    for item in basket_instance:  # Calls __iter__()
    print(f"Product: {item['product'].name}, Quantity: {item['qty']}, Total Price: {item['total_price']}")
    '''
    
    def __len__(self):
        """
        Get the basket session data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def update(self, product, qty):
        """
        Update values in basket session data
        """
        # product_id = str(product)
        product_id = product #just remember this 'product' is the product ID and not the actual product data from the database.
        # qty = qty #we don't have to do that necessarily, but just lay it out there so we have got these two parameters.
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()
    
    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = product

        if product_id in self.basket: #'product_id' considered as a key in this dictionary so this conditional statement checks if 'product_id' key exists in 'self.basket'
            del self.basket[product_id] # This effectively removes the item identified by 'product_id'.
            #if the type of this 'product_id' is an integer, when we try and run against the data that's stored in the basket session data, the id of the product is stored there as a string, so by the above line in this case we're trying to compare an integer with a string and that's not making the match, so we need to cast this integer as a string by "product_id = str(product.id)".(in our case but there's no need to be concerned 'cause the type of our 'product_id' is already a string.)
            print(product_id) #If I use print here it means that when I reload the page and then delete an item, I can see the ID of the deleted product within the terminal.
            print(type(product_id)) #<class 'str'>
            self.save() #After deleting the item, this line calls a method named 'save()' on self. This method likely persists changes to the session data (e.g., updating a database or session storage) to ensure that the deletion is reflected in future interactions.

    def save(self): #telling jango that we've made a change in our session data 
        self.session.modified = True
    
    # def get_item_total_price(self):
    #     return (Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())  
    
    def get_item_total_price(self, product_id):
        """
        Calculate the total price for a specific item in the basket.
        
        :param product_id: The ID of the product to calculate the total price for.
        :return: The total price for the specified product.
        """
        # Check if the product is in the basket
        if str(product_id) in self.basket:
            item = self.basket[str(product_id)]
            return Decimal(item['price']) * item['qty']
        
        # If the product is not in the basket, return 0
        return Decimal('0.00')
'''
Explanation
Session vs. Cookie:
Session: In web applications, a session is a server-side storage mechanism that maintains user state across multiple requests. Each session is identified by a unique session ID, which is often stored in a cookie on the client side.
Cookie: A cookie is a small piece of data stored on the client's browser. It can be used to store session IDs or other information that needs to persist across requests.
How It Works:
When a user interacts with a web application, the server creates a session and assigns it a unique identifier (session ID). This session ID is sent to the user's browser as a cookie (e.g., sessionid).
The server uses this session ID to retrieve the corresponding session data for that user. The actual data stored in the session can include various pieces of information, such as user preferences or items in a shopping basket.
The Role of 'skey':
In your code, 'skey' is simply a key that you have chosen to use to access a specific piece of data within the session (in this case, likely related to the shopping basket).
It does not directly refer to the name of the cookie itself but rather to an entry within the session storage that may or may not be tied to cookie values.


The phrase "maintains user state across multiple requests" refers to the ability of a web application to remember and preserve certain information about a user as they navigate through different pages or make various requests during a single session. Here’s a detailed explanation of what this means:
Explanation
Stateless Nature of HTTP:
The Hypertext Transfer Protocol (HTTP) is inherently stateless, meaning that each request from a client (like a web browser) to a server is treated as an independent transaction. The server does not retain any information about previous requests once it has responded to them.
User State:
User state can include various types of information such as:
Authentication status (whether the user is logged in or not)
User preferences (like language settings or themes)
Shopping cart contents in an e-commerce application
Any other data relevant to the user's session
Session Management:
To overcome the stateless nature of HTTP and maintain user state, web applications use session management techniques. This involves creating a session for each user when they first interact with the application.
A unique session identifier (session ID) is generated and sent to the client, usually stored in a cookie. This ID allows the server to recognize subsequent requests from the same user.
Maintaining State Across Requests:
When a user makes multiple requests (e.g., clicking links, submitting forms), the server can use the session ID to retrieve the corresponding session data stored on the server. This allows the application to provide a seamless experience by remembering the user's state.
For example, if a user adds items to their shopping cart on one page and then navigates to another page, the application can retrieve the contents of their cart using the session data, thus maintaining continuity in their experience.
Importance
User Experience: Maintaining user state enhances the user experience by allowing users to interact with an application without losing context. For instance, they can log in once and remain logged in as they browse different sections of a website.
Security: Session management also plays a crucial role in security, allowing applications to track authenticated users and manage permissions effectively.
Summary
In summary, "maintains user state across multiple requests" means that web applications use session management techniques to remember information about users as they interact with different parts of the application. This capability is essential for providing a cohesive and personalized experience while overcoming the limitations of HTTP's stateless nature.
'''

'''
Session ID
Definition:
A session ID (also known as a session token) is a unique identifier assigned to a user session by the server. It is used to track the user's interactions with the web application over a period of time.
Purpose:
The session ID allows the server to recognize requests from the same user, enabling continuity in operations (e.g., maintaining login status, tracking items in a shopping cart).
Storage:
The session ID is typically stored in a cookie on the user's browser. When the user makes requests to the server, this cookie is sent along, allowing the server to retrieve the corresponding session data.
Security Considerations:
Session IDs should be randomly generated and complex enough to prevent guessing or brute-force attacks. They should not contain sensitive information and should be protected during transmission.
Lifecycle:
The lifecycle of a session ID is controlled by the server, which can expire it after a certain period of inactivity or upon user logout.
'''

'''
Understanding Session Management
Session ID vs. Session Key:
Session ID: This is a unique identifier generated by the server when a session is created. It distinguishes one session from another and is typically stored in a cookie on the client side. The session ID is sent with each request to allow the server to retrieve the corresponding session data.
Session Key: This term can refer to various things depending on context, but in your example, it seems to refer to a specific key used within the session data (like 'skey') to access particular information (e.g., a shopping basket).
How the Server Identifies Sessions:
When a user interacts with a web application, the server generates a session ID and sends it to the client as a cookie. This cookie is included in subsequent requests made by the client.
The server uses this session ID to look up the corresponding session data stored on its side (in memory, database, etc.). This means that even if you do not explicitly name your session (like using 'skey'), the server can still identify which session belongs to which user based on the session ID stored in cookies.
Using Keys Within Sessions:
The key 'skey' in your code is used to access specific data within that user's session. For example, if you have a shopping basket, you might store its contents under this key.
If 'skey' does not exist in the session, you can initialize it (as shown in your initial code snippet). The server understands that when you call self.session.get('skey'), you're asking for data associated with that specific key within the context of the current user's active session.

'''

'''
Nested Sessions:
The idea of having a "session within a session" could refer to managing multiple states or contexts for the same user. However, traditional session management does not inherently support this structure.
Instead, you might manage different contexts (like user roles or specific activities) within the same session using different keys or attributes in the session data.
Use Cases:
For example, in an e-commerce application, you might have a main session for the user and then manage different contexts like:
A shopping cart (stored under a key like 'cart')
User preferences (stored under another key)
Temporary data for a checkout process (stored under yet another key)
'''

'''
An instance variable is a variable that is defined within a class but outside any method. 
It is associated with a specific instance (or object) of that class, meaning that each object has its own copy of the instance variable. 

Instance variables are declared inside a class definition. For example, in Python, they are typically initialized within the __init__ method (the constructor) using the self keyword:
python
class Shark:
    def __init__(self, name, age):
        self.name = name  # Instance variable
        self.age = age    # Instance variable

Unique to Each Instance:
Each object created from a class has its own set of instance variables. This means that changes to an instance variable in one object do not affect the same variable in another object. For example:
python
shark1 = Shark("Sammy", 5)
shark2 = Shark("Stevie", 8)

print(shark1.name)  # Output: Sammy
print(shark2.name)  # Output: Stevie

In this case, shark1 and shark2 have their own copies of the name and age instance variables.
Instance variables are accessible throughout the methods of the class via the 'self' reference. They can be used to store data that is specific to an instance of the class.
'''




'''
break down the '__iter__' method of the Basket class step by step using an example instance of the Basket class and your Product model. 
(in WordPad)
'''