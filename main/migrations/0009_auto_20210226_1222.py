# Generated by Django 3.1.6 on 2021-02-26 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210225_1819'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categoryfeature',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='categoryfeature',
            name='category',
        ),
        migrations.RemoveField(
            model_name='featurevalidator',
            name='category',
        ),
        migrations.RemoveField(
            model_name='featurevalidator',
            name='feature_key',
        ),
        migrations.RemoveField(
            model_name='productfeatures',
            name='feature',
        ),
        migrations.RemoveField(
            model_name='productfeatures',
            name='product',
        ),
    ]
