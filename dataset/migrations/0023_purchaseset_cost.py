# Generated by Django 4.1.7 on 2023-04-05 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0022_rename_due_purchaseset_net'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseset',
            name='cost',
            field=models.FloatField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
