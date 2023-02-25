# Generated by Django 4.1.3 on 2023-01-12 07:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Pay Due',
            },
        ),
        migrations.AlterField(
            model_name='sellset',
            name='client',
            field=models.CharField(choices=[('1', 'Resort'), ('2', 'Restaurant'), ('3', 'Kitchen'), ('4', 'House-Keeping'), ('5', 'Hall_Room'), ('6', 'Swimming-Pool'), ('7', 'Public-Amt'), ('8', 'Driver'), ('9', 'Passport')], default=1, max_length=2),
        ),
        migrations.CreateModel(
            name='PurchasePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(blank=True, max_length=250, null=True)),
                ('amount', models.FloatField(max_length=10)),
                ('total_amount', models.FloatField(max_length=10)),
                ('date', models.DateField(default=datetime.date.today)),
                ('pay', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pay_fk', to='dataset.pay')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_fk2', to='dataset.purchaseset')),
            ],
            options={
                'verbose_name_plural': 'Purchase Payment',
            },
        ),
    ]