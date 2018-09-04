from django.db import models
from django.contrib.auth import models.User as User
from openfoodfacts.models import Product

class favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "favori"

    def __str__(self):
        return self.products
