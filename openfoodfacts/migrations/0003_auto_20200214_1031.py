# Generated by Django 3.0.3 on 2020-02-14 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openfoodfacts', '0002_product_popularity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img_nutrinfo_url',
            field=models.URLField(max_length=2100, null=True, verbose_name='Image des informations nutritionnelles'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img_url',
            field=models.URLField(max_length=2100, null=True, verbose_name='Image du produit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='product',
            name='nutriscore',
            field=models.CharField(max_length=1, verbose_name='Nutriscore'),
        ),
        migrations.AlterField(
            model_name='product',
            name='off_url',
            field=models.URLField(max_length=2100, null=True, verbose_name='Lien vers la page Openfoodfacts'),
        ),
        migrations.AlterField(
            model_name='product',
            name='popularity',
            field=models.IntegerField(null=True, verbose_name='Score de popularité'),
        ),
    ]
