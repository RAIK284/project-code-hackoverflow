from django.db import models
from messaging.models import Profile

class Product(models.Model):
    """Model representing an item in the store."""
    name = models.CharField(max_length=50)
    point_cost = models.IntegerField()
    amount_sold = models.IntegerField()
    image = models.ImageField(upload_to='product_images/') # TODO: How to fetch

    class Meta:
        # Order items alphabetically by default
        ordering = ['name']

    def __str__(self):
        return self.name

class Purchase(models.Model):
    """Model controlling the relationship between a user and their purchased item."""
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer}: {self.product}"
