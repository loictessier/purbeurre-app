from django.db import models


class Category(models.Model):
    name = models.CharField('Nom', max_length=200, unique=True)
    off_identifier = models.CharField('Identifiant Openfoodfacts', max_length=200)

    class Meta:
        verbose_name = "categorie"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Nom', max_length=200, unique=True)
    nutriscore = models.CharField('Nutriscore', max_length=1)
    img_nutrinfo_url = models.URLField('Image des informations nutritionnelles', max_length=2100, null=True)
    img_url = models.URLField('Image du produit', max_length=2100, null=True)
    off_url = models.URLField('Lien vers la page Openfoodfacts', max_length=2100, null=True)
    popularity = models.IntegerField('Score de popularité', null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='categorie')

    class Meta:
        verbose_name = "aliment"

    def __str__(self):
        return self.name
