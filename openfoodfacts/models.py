from django.db import models

class Product(models.Model):
    name = models.CharField('name', max_length=200, unique=True)
    nutriscore = models.CharField('nutriscore', max_length=1)
    img_nutrinfo_url = models.URLField('img_nutrinfo_url', max_length=2100, null=True)
    img_url = models.URLField('img_url', max_length=2100, null=True)
    off_url = models.URLField('off_url', max_length=2100, null=True)
    
    class Meta:
        verbose_name = "aliment"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('name', max_length=200, unique=True)
    off_identifier = models.CharField('off_identifier', max_length=200)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)

    class Meta:
        verbose_name = "categorie"

    def __str__(self):
        return self.name
