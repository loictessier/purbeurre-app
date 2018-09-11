from django.db import models
from django.contrib.auth.models import User
from openfoodfacts.models import Product


class Profile(models.model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    # TODO avatar (+ champs supplémentaires éventuels voir doc)

    class Meta:
        verbose_name = "profil"

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "favori"

    def __str__(self):
        return self.product.name
