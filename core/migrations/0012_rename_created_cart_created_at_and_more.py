# Generated by Django 4.1.7 on 2023-04-11 08:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_cart_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='updated',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ordered',
        ),
        migrations.AddField(
            model_name='cart',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
