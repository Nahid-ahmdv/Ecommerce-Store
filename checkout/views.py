import json
import uuid
from account.models import Address
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from orders.models import Order, OrderItem
from django.conf import settings
from .models import DeliveryOptions


#zariiin
from django.conf import settings
import requests

@login_required
def deliverychoices(request): #Here what we need to do is we need to collect the data from the 'DeliveryOptions' model all the delivery options and return that (send that back) in this view (to the template).
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
#This is where we’re gonna send the (AJAX) request to the 'basket_update_delivery' function (view) .
def basket_update_delivery(request):
    basket = Basket(request) #I bring in the 'Basket' class (part of session data), now by instantiating the 'Basket' class we have access to the user basket session data!so now we can use some of the methods we've setup in 'Basket' class.
    #'basket' variable either contains a dictionary like '{'product_id_1': {'price': '10.00', 'qty': 2}, 'product_id_2': {'price': '15.50', 'qty': 1}, ...}' or an empty dictionary '{}'.
    '''
    The variable 'basket' will contain an instance of the 'Basket' class.
    The attribute 'self.basket' within that instance will hold either:
        The existing dictionary associated with 'skey', if it exists (representing items in the user's shopping basket).
        An empty dictionary if 'skey' did not exist in session data prior to this point.
    '''
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option) #so 'delivery_type' is a record in 'DeliveryOptions' table.
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True #We need to tell Django that we have changed the session so we need to set ‘session.modified = True’ (because we have made changes that’s what we have added.)

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})#A JSON response (dictionary format) is created containing the delivery and total price of the purchase.
        return response #Finally, this returns the JSON response back to the client (via AJAX), allowing it to update dynamically without reloading the page.
        #we use JSON because it returns the data in a format that we can then utilize within JavaScript (dictionary format).


@login_required
def delivery_address(request):

    session = request.session #This line retrieves the session object associated with the current user. The session is used to store temporary data that persists across requests, so we're gonna grab the session data and then create an 'if' statement:
    if "purchase" not in request.session: #"purchase" is a key in user session data dictionary which its corresponding value is the user selected delivery option.
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
        #If "purchase" is not found, it means that the user has not made a delivery option selection yet. A success message is added to inform the user to select a delivery option.
        #The view then redirects the user back to the previous page using 'HTTP_REFERER', which contains the URL of the page that referred the request.
    
    addresses = Address.objects.filter(customer=request.user).order_by("-default") #.order_by("-default") is used to sort the queryset of addresses retrieved from the database based on the 'default' field of the Address model.
    #When using "-default", addresses that have default=True will appear first in the list because they are considered "higher" in sorting order compared to those with default=False.

    
    #Save address in user session data:
    if "address" not in request.session: #The code checks if there is an "address" key in the session.
        session["address"] = {"address_id": str(addresses[0].id)} #If it does not exist, it initializes it with a dictionary containing the ID of the first address (which is selected address) from the retrieved list (addresses.id). This assumes that there is at least one address available.

    else: #If "address" already exists in the session, it updates the "address_id" with the ID of the first address (which is selected address) again.
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True #This line indicates that the session data has been modified and should be saved back to the database.


    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "checkout/payment_selection.html", {})


####
# PayPay
####
# from paypalcheckoutsdk.orders import OrdersGetRequest

# from .paypal import PayPalClient


@login_required
def payment_complete(request):
    # PPClient = PayPalClient()

    # body = json.loads(request.body)
    # data = body["orderID"]
    # user_id = request.user.id

    # requestorder = OrdersGetRequest(data)
    # response = PPClient.client.execute(requestorder)

    # total_paid = response.result.purchase_units[0].amount.value

    # basket = Basket(request)
    # order = Order.objects.create(
    #     user_id=request.user.id,
    #     full_name=response.result.purchase_units[0].shipping.name.full_name,
    #     email=response.result.payer.email_address,
    #     address1=response.result.purchase_units[0].shipping.address.address_line_1,
    #     address2=response.result.purchase_units[0].shipping.address.admin_area_2,
    #     postal_code=response.result.purchase_units[0].shipping.address.postal_code,
    #     country_code=response.result.purchase_units[0].shipping.address.country_code,
    #     total_paid=response.result.purchase_units[0].amount.value,
    #     order_key=response.result.id,
    #     payment_option="paypal",
    #     billing_status=True,
    # )
    # order_id = order.pk


# Retrieve basket and session data
    basket = Basket(request)

    # Extract user ID from session data
    # user_id = request.session.get('_auth_user_id')
    
    # Get user instance
    # user = UserBase.objects.get(pk=user_id)  # Fetching the user by ID
    user=request.user
    # Extract address details from session data
    address_id = request.session['address']['address_id']  # Get the address ID from session data
    address = Address.objects.get(id=address_id)  # Fetching the address instancel
    order_key = request.POST.get('order_key')
    # Create an Order instance in the database:
    if Order.objects.filter(order_key=order_key).exists():
        pass
    else:
        order = Order.objects.create(
            user=user,  # Use the user object directly
            full_name=address.full_name,  # Full name from Address model
            email=user.email,  # User's email from User model
            address1=address.address_line,  # Address line 1 from Address model
            address2=address.address_line2,  # Address line 2 from Address model
            city=address.town_city,  # Town/City/State from Address model
            phone=address.phone,  # Phone number from Address model
            postal_code=address.postcode,  # Postcode from Address model
            country_code='US',  # Replace with actual country code if available or adjust as needed
            total_paid=basket.get_ttotal_price(),  # Assuming you have this method in your Basket class to get total price
            order_key=uuid.uuid4(),  # Generate a new UUID for each paid order (optional since it's auto-generated by the model).
            payment_option='PayPal',  # Or whatever payment option was used
            billing_status=True,
        )

        order_id = order.pk #because we want to connect the 'Product' table to the 'Order' table, we can use the order primary key to loop through the data inside of user session and add all those products (items that user has bought) to the 'OrderItem' table.

        for item in basket:
            OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])
            '''
            Here, 'order_id=order_id' is actually passing the value of 'order_id' to the order field of the 'OrderItem' model. Django automatically understands that when you pass 'order_id=...', it should look for a foreign key field named 'order'.
            '''
    return JsonResponse("Payment successful!", safe=False)


@login_required
def payment_successful(request):
    # Get the latest order for the logged-in user
    latest_order = Order.objects.filter(user=request.user).order_by('-created').first()  # Get the most recent order
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {'latest_order': latest_order})



# ############################################
# #? sandbox merchant 
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'


# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8080/verify/'


# def send_request(request):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Description": description,
#         "Phone": phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return JsonResponse({'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']})
#             else:
#                 return JsonResponse({'status': False, 'code': str(response['Status'])})
#         return JsonResponse({'status': False, 'code': 'Invalid response'})
        
#     except requests.exceptions.Timeout:
#         return JsonResponse({'status': False, 'code': 'timeout'})
#     except requests.exceptions.ConnectionError:
#         return JsonResponse({'status': False, 'code': 'connection error'})


# def verify(authority):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
#     response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             return {'status': True, 'RefID': response['RefID']}
#         else:
#             return {'status': False, 'code': str(response['Status'])}
#     return response