from django.db import models

from user.models import Profile
from openfoodfacts.models import Product


# Create your models here.
class RatingProduct(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField('Note', null=False)

    class Meta:
        verbose_name = "note"

    def __str__(self):
        return str(self.rating)
