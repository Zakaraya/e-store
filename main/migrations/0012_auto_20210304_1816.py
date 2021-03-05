# Generated by Django 3.1.6 on 2021-03-04 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_remove_order_customer'),
        ('specification', '0001_initial'),
        ('main', '0011_auto_20210304_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='features',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.categoryproduct', verbose_name='Категория'),
        ),
        migrations.DeleteModel(
            name='Iphone',
        ),
    ]