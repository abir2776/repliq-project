# Generated by Django 4.1.7 on 2023-04-09 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_user_category_product_price_shop_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]