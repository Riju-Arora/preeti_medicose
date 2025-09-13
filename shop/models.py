

# Create your models here.
from django.db import models
# shop/models.py

from decimal import Decimal
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('medicine', 'Medicine'),
        ('cosmetic', 'Cosmetic'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(default="", blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    def discount_percent(self):
        if self.mrp and self.price and self.mrp > self.price:
            return round(((self.mrp - self.price) / self.mrp) * 100, 2)
        return 0


    def __str__(self):
        return self.name




class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"






