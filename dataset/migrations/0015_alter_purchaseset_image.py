# Generated by Django 4.1.3 on 2023-02-06 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0014_purchaseset_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseset',
            name='image',
            field=models.ImageField(null=True, upload_to='voucher'),
        ),
    ]