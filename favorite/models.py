from django.db import models
from user.models import Profile


class Favorite(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey('openfoodfacts.Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "favori"

    def __str__(self):
        return self.product.name
