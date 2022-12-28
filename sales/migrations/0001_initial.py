# Generated by Django 4.1.3 on 2022-12-28 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecommerce', '0002_category_origin_packing_warehouse_product_customers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesParent',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('invoice_no', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('due_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('status', models.CharField(default='Open', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ecommerce.customers')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ecommerce.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='SalesChild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('packing_qty', models.DecimalField(decimal_places=2, default=1, max_digits=20)),
                ('packing', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('packing_unit', models.CharField(blank=True, max_length=20, null=True)),
                ('extra_field', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('is_active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('invoice_no', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sales.salesparent')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ecommerce.products')),
            ],
            options={
                'unique_together': {('product', 'invoice_no')},
            },
        ),
    ]
