# Generated by Django 4.1.7 on 2023-04-11 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_cart_user_cart_shop_alter_order_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='shop',
        ),
    ]