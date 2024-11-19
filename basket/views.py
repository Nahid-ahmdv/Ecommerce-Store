from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse

from store.models import Product

from .basket import Basket

app_name = 'basket' #same as the 'namespace' of the path referred to this directory that I wrote in 'core/urls.py'.

# Create your views here.

def basket_summary(request): # This 'request' is an instance of 'HttpRequest' which contains the details of user request.
    basket = Basket(request) #to be able to grab the user's basket session data (remember we're instantiating the 'Baket' class here. In other word, an instance of the 'Basket' class is created using the incoming 'request'. This initializes the session and retrieves or creates the user's basket.)
    return render(request, 'store/basket/summary.html', {'basket': basket}) #we're gonna create a new folder is 'templates/store' folder called 'basket' and inside that a page called 'summary.html'.





#some data within a AJAX request (been created in 'singleproduct.html') is gonna be sent off to this view and we need to collect the data that's been sent to this view from our page ('singleproduct.html'):
def basket_add(request): #This defines a function named 'basket_add', which handles adding items to the shopping basket. It takes an HTTP request as an argument.
    #we're gonna need to access to user's basket session data so first of all we grab that.
    basket = Basket(request) #Here, an instance of the 'Basket' class is created using the incoming 'request'. This initializes the session and retrieves or creates the user's basket.
    #if request.method == 'POST':
    #or
    if request.POST.get('action') == 'post':  #This checks if the action specified in the 'POST' request is 'post' which means that if the request l've received from AJAX is a POST request, indicating that this function should process an addition to the basket (we can change the value of 'action' key to whatever we want (other that 'post') in AJAX request and here).
        #When a user submits a form on a webpage, any input fields within that form are sent to the server as part of the POST request.
        #Each input field's name attribute becomes a key in the 'request.POST' dictionary, and its value becomes the corresponding value.
        
        product_id = int(request.POST.get('productid')) #collecting the product id from the AJAX request data #This retrieves the product ID from the AJAX request data and converts it to an integer.
        product_qty = int(request.POST.get('productqty')) #Similarly, this retrieves and converts the product quantity from the 'POST' data.
        #now l've got the actuall product id I can now actually find the product in the database ('Product' model):
        product = get_object_or_404(Product, id=product_id) #we collected that product via its id. Therefor, we have access to all of its information.#This line attempts to retrieve a Product object from the database using its ID. If no product with that ID exists, it raises a 404 error (not found).
        #now we're gonna save that product_id and its qty to the user's session (in actual fact there is a main session for the user and different contexts are gonna be managed and stored under different keys. in our case we stored our data (the product_id and its qty) under a key named 'skey' and put them in a variable called 'basket').
        #'skey' is simply a key that we have chosen to use to access a specific piece of data within the session (in this case, related to the shopping basket).
        basket.add(product=product, qty=product_qty) #This calls a method to add and save the specified product (product_id) and quantity to the basket.
        
        #Building a response to send the data back to the front-end (user) to gonna be available via the front-end:
        #we're now gonna build a response (sending the data back to the user) and what we're gonna return back is the new updated basket quantity:
        basketqty = basket.__len__() #This retrieves the total number of items in the basket by calling ' __len__()' method on the basket.
        # basketqty = sum(item['qty'] for item in basket.basket.values())
        response = JsonResponse({'qty': basketqty}) #A JSON response (dictionary format) is created containing the total quantity of items in the basket.
        return response #Finally, this returns the JSON response back to the client (via AJAX), allowing it to update dynamically without reloading the page.
        #we use JSON because it returns the data in a format that we can then utilize within JavaScript (dictionary format).

# def basket_add(request):
#     if request.method == 'POST':
#         basket = Basket(request)

#         # Get product ID and quantity from POST data
#         product_id = request.POST.get('productid')
#         product_qty = request.POST.get('productqty')

#         if not product_id or not product_qty:
#             return JsonResponse({'error': 'Missing product ID or quantity'}, status=400)

#         try:
#             product_id = int(product_id)
#             product_qty = int(product_qty)
#         except ValueError:
#             return JsonResponse({'error': 'Invalid product ID or quantity'}, status=400)

#         # Retrieve the Product instance
#         product = get_object_or_404(Product, id=product_id)

#         # Add the product to the basket
#         basket.add(product=product, qty=product_qty)

#         # Get the total quantity in the basket
#         basketqty = sum(item['qty'] for item in basket.basket.values())

#         # Return the updated quantity as JSON response
#         return JsonResponse({'qty': basketqty})

#     return JsonResponse({'error': 'Invalid request method'}, status=405)  # Method Not Allowed

'''
The 'Basket' class (within 'basket.py') handles session management for storing items in a user's cart, 
while the 'basket_add' function processes requests to add items to that cart and returns feedback about how many items are currently in it.

in 'Basket' class The instance variables 'self.basket' and 'self.session' are set based on the session data.
This means that every instance of 'Basket' class will have its own session and basket, which are initialized based on the current user's request.
'''

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
the basket.__len__() method would return the number of unique products currently stored in the basket, not the total quantity of all items. in the above example, there are two unique product IDs in the basket: '1' and '2'.
Therefore, calling basket.__len__() would return 2.
If you wanted to get the total quantity of all items in the basket (which is often what users think of when considering the "length" of a basket), you would need to sum the quantities of each product. Here’s how you could do that:
python
total_quantity = sum(item['qty'] for item in self.basket.values())

In your example:
For Product ID '1', the quantity is 3.
For Product ID '2', the quantity is 1.
So, the total quantity would be:
Total Quantity = 3 (from product ID 1) + 1 (from product ID 2) = 4
'''
# def basket_update(request):
#     basket = Basket(request)
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('productid'))
#         product_qty = int(request.POST.get('productqty'))
#         basket.update(product=product_id, qty=product_qty)

#         basketqty = basket.__len__()
#         baskettotal = basket.get_total_price()
#         response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
#         return response
def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        # product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty')) 
        product_id = request.POST.get('productid') #we're gonna get the ID of the product which is gonna be getting updated and the quantity from the AJAX request data. 
        # Update the quantity in the basket
        print(product_qty)
        print(product_id)
        basket.update(product=product_id, qty=product_qty) #updating the data within our session data

        # Get updated quantities and prices
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        print(baskettotal)
        # Calculate the total price for this specific item
        item_total_price = basket.get_item_total_price(product_id)  # Implement this method as needed
        #we use 'response' to send the data back.
        response = JsonResponse({
            'qty': basketqty,
            'baskettotal': baskettotal,
            'item_total_price': item_total_price  # Send back the updated total price for this item
        })
        
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        # product_id = int(request.POST.get('productid'))
        product_id = request.POST.get('productid') #we don't need to convert it to int 'cause all we need in this function an the method definded in 'Baket'class called 'delete' is str version of it, which because of this line in the summary.html file 'var prodid = $(this).data('index');' is already str.
        
        # Update the quantity in the basket
        basket.delete(product=product_id)

        # Get updated quantities and prices
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        
        # Calculate the total price for this specific item
        # item_total_price = basket.get_item_total_price(product_id)  # Implement this method as needed

        response = JsonResponse({
            'qty': basketqty,
            'baskettotal': baskettotal,
            # 'item_total_price': item_total_price  # Send back the updated total price for this item
        })
        
        return response