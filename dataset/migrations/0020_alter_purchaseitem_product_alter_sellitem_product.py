# Generated by Django 4.1.7 on 2023-04-05 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0019_alter_purchaseitem_product_alter_sellitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_fk', to='dataset.product'),
        ),
        migrations.AlterField(
            model_name='sellitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_fk2', to='dataset.product'),
        ),
    ]
