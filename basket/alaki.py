# from store.models import Product

basket = {'8': {'price': '15.99', 'qty': 4}, '7': {'price': '12.99', 'qty': 3}, '4': {'price': '13.99', 'qty': 1}, '3': {'price': '8.98', 'qty': 1}, '6': {'price': '24.99', 'qty': 2}, '5': {'price': '33.49', 'qty': 1}}
print(type(basket))

if '8' in basket:
    print("jjjjjjjjj")
# product_ids = basket.keys()
# print(type(product_ids))
# print(product_ids)


# basket['8']['product'] = 'product'
# print(basket, '   ')


# for product in basket: 
#     basket[product]['product'] = 'product'
# print(basket, '\n\n')

# for product in basket: 
#     print(type(product))

# for product_id in basket: 
#     print(basket[product_id]['qty']) 

# for item in basket.values():
#     print(item)
#When you iterate over a dictionary using a loop like for item in basket:, the variable item will actually hold the keys of the dictionary (in this case, the product IDs like '8', '7', etc.). If you want to access the corresponding value (which is itself a dictionary), you need to use square brackets with the key.