from django.db import models
from user.models import Profile

from openfoodfacts.models import Product


class Favorite(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey('openfoodfacts.Product', related_name="substitute", on_delete=models.CASCADE)
    origin_product = models.ForeignKey('openfoodfacts.Product', related_name="origin_product", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "favori"

    def __str__(self):
        return self.product.name
