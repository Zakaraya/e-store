# Generated by Django 3.1.3 on 2020-12-19 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
    ]