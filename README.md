TASKS FROM TEST ASSIGNMENT TO WRITE QUERIES IN DJANGO ORM AND RAW SQL.

Project description: project is a marketplace with the main entities:

products (Product model).
Each product has the name, and several additional parameters. There are products with the same name but different sellers.

users (User model).
The standard Django User model. Users can be sellers at the same time. Each user can sell an unlimited number of products or may not sell anything.

orders (Order and OrderItem models).
When a new order is added, a new Order instance is created. Product items are linked to it through the intermediate OrderItem model. Each OrderItem has links with the product and the order. Also there is a quantity field - number of particular product units in the order.

########
TASK 1:
Django ORM. Write the query to return the list of dicts with product names and total count of ordered products. Sort them from the most sellable to the least sellable products.

Example:

[
    {'product': '...', 'ordered_count': ...},
    {'product': '...', 'ordered_count': ...},
    ...
]


SOLUTION:

Product.objects.values('name').annotate(ordered_items=Sum('order_items__quantity')).order_by('-ordered_items')

########
TASK 2: 
Implement the task 1 in the raw SQL:

SOLUTION:
"""
    SELECT product.name, SUM(order_item.quantity) as orders_number
    FROM marketplace_product product
    LEFT JOIN marketplace_orderitem order_item
    ON product.id = order_item.product_id
    GROUP BY product.name
    ORDER BY orders_number DESC;
"""

########
TASK 3:
Write the query to return the list of dicts with seller usernames and the number of products they sell.


SOLUTION:

User.objects.values('username').annotate(products_count=Count('selling_products'))

#Product.objects.values('seller__username').annotate(product_count=Count('id'))

########
TASK 4: 
Write the raw SQL query to get the full list of products. It should contain the following columns:

Product name
Manufacturer
Price
Seller username

SOLUTION: 
"""
    SELECT product.name, manufacturer.name, product.price, user.username
    FROM marketplace_product product
    LEFT JOIN marketplace_manufacturer manufacturer
    ON product.manufacturer_id = manufacturer.id
    LEFT JOIN auth_user user
    ON product.seller_id = user.id;
"""

########
TASK 5:
Task: Write the query to return the list of dicts with product name and the total sum (in currency) of ordered products. Sort them from the most sellable to the least sellable products.

Note 1: return zero if a product was not sold yet.

Note 2: to calculate the total ordered price you need to calculate the sum of all order items price * quantity.

Example:

[
    {'name': '...', 'total_ordered': ...},
    {'name': '...', 'total_ordered': ...},
]


SOLUTION:
Product.objects.values('name', 'price')\
        .annotate(total_ordered=Sum(F('order_items__quantity') * F('price')))

########
TASK 6: 
Implement the task 5 in the raw SQL:

SOLUTION:
 SQL = """
        SELECT product.name, product.price, Sum(order_item.quantity) as items_ordered,
        Sum(order_item.quantity * product.price) as total_sum
        FROM marketplace_product product
        LEFT JOIN marketplace_orderitem  order_item
        ON product.id = order_item.product_id
        GROUP BY product.name
        ORDER BY total_sum DESC;
        """