# Generated by Django 4.1.3 on 2022-12-20 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='unit_set',
            new_name='unit',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='unit_value',
            new_name='value',
        ),
    ]