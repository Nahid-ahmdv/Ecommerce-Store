#we want the user's basket to be available throughout our project, so we made a context_processor.py.
from .basket import Basket

'''
What is happening here is that we’re gonna pass this request data into the ‘Basket’ class so that we can utilize it, 
because we need that information. When the user sends data from the browser, they type in whatever domain or whatever page they’re looking for, they actually send that HTTP request instance over to Django and now that’s all in the ‘request’, 
and that data is the ‘request’ (the session information is inside of that ‘request’) so that we can grab the information inside of the ‘request’ and check the session if it exists and then return some data.
'''
def basket(request): #Here, a function named basket is defined, which takes one parameter, request. This parameter typically represents an HTTP request object, which contains information about the incoming request, including session data.
    return {'basket': Basket(request)} #what is return is the value associated with 'basket' key which is whatever in the basket of the user (the instance variable that was defined within basket.py 'Basket' class).
'''
Inside the function, it creates an instance of the 'Basket' class by passing the 'request' object to its constructor (__init__).
The function returns a dictionary with a single key-value pair:
The key is 'basket'.
The value is the instance of the 'Basket' class created using the provided request.
'''

'''
By returning a dictionary with the key 'basket', this function allows templates to easily access the 'Basket' instance.
For example, in a Django view, you might use this function to ensure that every template has access to the user's shopping basket or cart.
Dependency Injection:
By passing the 'request' object to the 'Basket', this design allows the 'Basket' class to manage user-specific data (like items in a shopping cart) based on the current session associated with that request.
'''