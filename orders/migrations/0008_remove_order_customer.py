# Generated by Django 3.1.3 on 2020-12-19 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
    ]
