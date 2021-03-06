# Generated by Django 3.0.6 on 2020-07-06 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('openfoodfacts', '0004_auto_20200214_1100'),
        ('user', '0003_auto_20200203_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(verbose_name='Note')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openfoodfacts.Product')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Profile')),
            ],
            options={
                'verbose_name': 'note',
            },
        ),
    ]
