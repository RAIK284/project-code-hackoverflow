from django.contrib import admin
from .models import Product, Purchase

# Register models to use on admin page
admin.site.register(Product)
admin.site.register(Purchase)
