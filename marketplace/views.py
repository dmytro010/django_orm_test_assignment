from django.db import connection
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F

def task_1_view(request):
  
    query = Product.objects.values('name')\
        .annotate(ordered_items=Sum('order_items__quantity'))\
            .order_by('-ordered_items')

    return JsonResponse({'result': list(query)})

def task_2_view(request):
  
    SQL = """
    SELECT product.name, SUM(order_item.quantity) as orders_number
    FROM marketplace_product product
    LEFT JOIN marketplace_orderitem order_item
    ON product.id = order_item.product_id
    GROUP BY product.name
    ORDER BY orders_number DESC;
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL)
        result = cursor.fetchall()

    return JsonResponse({'result': result})

def task_3_view(request):

    query = User.objects.values('username')\
        .annotate(products_count=Count('selling_products'))
    return JsonResponse({'result': list(query)})

def task_4_view(request):
  
    SQL = """
        SELECT product.name, manufacturer.name, product.price, user.username
        FROM marketplace_product product
        LEFT JOIN marketplace_manufacturer manufacturer
        ON product.manufacturer_id = manufacturer.id
        LEFT JOIN auth_user user
        ON product.seller_id = user.id;
        """

    with connection.cursor() as cursor:
        cursor.execute(SQL)
        result = cursor.fetchall()

    return JsonResponse({'result': result})

def task_5_view(request):
    
    query = Product.objects.values('name', 'price')\
        .annotate(ordered_count=Sum('order_items__quantity'), 
        total_price=Sum(F('order_items__quantity') * F('price')))

    return JsonResponse({'result': list(query)})

def task_6_view(request):

    SQL = """
        SELECT product.name, product.price, Sum(order_item.quantity) as items_ordered,
        Sum(order_item.quantity * product.price) as total_sum
        FROM marketplace_product product
        LEFT JOIN marketplace_orderitem  order_item
        ON product.id = order_item.product_id
        GROUP BY product.name
        ORDER BY total_sum DESC;
        """

    with connection.cursor() as cursor:
        cursor.execute(SQL)
        result = cursor.fetchall()

    return JsonResponse({'result': result})
