# shop/admin.py
from django.contrib import admin
from .models import Product

# ------------- PRODUCT ADMIN -----------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns displayed in admin list
    list_display = ('name', 'category', 'price', 'mrp', 'discount_percent')
    
    # Fields you can search
    search_fields = ('name', 'description')
    
    # Filters
    list_filter = ('category',)
    
    # Pagination
    list_per_page = 50
    
    # Default ordering
    ordering = ('name',)

# ------------- SECURITY FOR ADMIN -----------------
# This is done in settings.py and urls.py

