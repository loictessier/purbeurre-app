from django.db import models
from user.models import Profile

from openfoodfacts.models import Product


class Favorite(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="substitute", on_delete=models.CASCADE, verbose_name='Produit favoris')
    
    class Meta:
        verbose_name = "favori"

    def __str__(self):
        return self.product.name
