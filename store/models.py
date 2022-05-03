from django.db import models
import os

def get_image_path(instance, filename):
    """
    Gets the system path for an image to display.
    
    Taken from: https://stackoverflow.com/a/8192232/5696057
    """
    return os.path.join('product_images', str(instance.id), filename)

class Product(models.Model):
    """
    Model representing an item in the store.
    
    Note: We want products to only be editable in the admin page.
    """
    name = models.CharField(max_length=50, unique=True)
    point_cost = models.IntegerField()
    amount_sold = models.IntegerField()
    image = models.ImageField(upload_to=get_image_path, null=True)
    
    class Meta:
        # Order items alphabetically by default
        ordering = ['name']

    def __str__(self):
        return self.name

class Purchase(models.Model):
    """Model controlling the relationship between a user and their purchased item."""
    buyer = models.ForeignKey("messaging.Profile", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer}: {self.product}"
