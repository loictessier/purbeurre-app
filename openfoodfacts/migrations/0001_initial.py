# Generated by Django 2.1 on 2018-09-26 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
                ('off_identifier', models.CharField(max_length=200, verbose_name='off_identifier')),
            ],
            options={
                'verbose_name': 'categorie',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
                ('nutriscore', models.CharField(max_length=1, verbose_name='nutriscore')),
                ('img_nutrinfo_url', models.URLField(max_length=2100, null=True, verbose_name='img_nutrinfo_url')),
                ('img_url', models.URLField(max_length=2100, null=True, verbose_name='img_url')),
                ('off_url', models.URLField(max_length=2100, null=True, verbose_name='off_url')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='openfoodfacts.Category')),
            ],
            options={
                'verbose_name': 'aliment',
            },
        ),
    ]
