# Generated by Django 4.1.7 on 2023-04-11 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
