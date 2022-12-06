from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    )

    name = models.CharField(max_length=75)
    manufacturer = models.ForeignKey(
        Manufacturer, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='selling_products',
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('new', 'New'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='orders',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    @property
    def total(self):
        return sum([x.total_price for x in self.items.all()])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

 
    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product} ⨉ {self.quantity}'

    @property
    def total_price(self):
        return self.price * self.quantity