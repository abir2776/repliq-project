# Generated by Django 4.1.7 on 2023-04-07 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_user_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='categorys', to='core.category'),
        ),
    ]