# Generated by Django 4.1.3 on 2023-01-24 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0012_rename_shop_sellset_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellset',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='client_fk', to='dataset.client'),
        ),
    ]
