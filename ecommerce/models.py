from django.db import models
from django.utils import timezone
from django.db.models import Sum
from datetime import date
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=250)
    delete_flag = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ecommerce of Brand"

    def __str__(self):
        return str(f"{self.name}")


class Products(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250, default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank= True, null= True)
    buy = models.FloatField(max_length=15, default=0)
    price = models.FloatField(max_length=15, default=0)
    mrp = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Ecommerce of Products"

    def __str__(self):
        return str(f"{self.name}")


class Purchase(models.Model):
    code = models.CharField(max_length=100)
    note = models.CharField(max_length=250, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="brand_fk5")
    total_amount = models.FloatField(max_length=15)
    status = models.CharField(max_length=2,
                              choices=(('0', 'Pending'), ('1', 'In-progress'), ('2', 'Done'), ('3', 'Picked Up')),
                              default=0)
    payment = models.CharField(max_length=2, choices=(('0', 'Unpaid'), ('1', 'Paid')), default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ecommerce of Purchase"

    def __str__(self):
        return str(f"{self.code} - {self.client}")

    def totalProducts(self):
        try:
            Products = PurchaseProducts.objects.filter(purchase=self).aggregate(Sum('total_amount'))
            Products = Products['total_amount__sum']
        except:
            Products = 0
        return float(Products)


class PurchaseProducts(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_fk2")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="purchase_fk")
    buy = models.FloatField(max_length=15, default=0)
    price = models.FloatField(max_length=15, default=0)
    quantity = models.FloatField(max_length=15, default=0)
    free_quantity = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)

    class Meta:
        verbose_name_plural = "Ecommerce of Purchase Products"

    def __str__(self):
        return str(f"{self.purchase.code} - {self.product.name}")


def customer_code():
    prifix = "RR-"
    next_number = '00001'
    last_number = Customers.objects.filter(customer_code__startswith=prifix).order_by('customer_code').last()
    if last_number:
        last_code = int(last_number.customer_code[4:])
        next_number = '{0:05d}'.format(last_code + 1)
    return prifix + next_number


class Customers(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    customer_code = models.CharField(max_length=20, primary_key=True, default=customer_code)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    bin_no = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.customer_name


class Origin(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    origin_name = models.CharField(max_length=50, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.origin_name


class Category(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


class Packing(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    packing_type = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='packing_author', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product Unit'
        verbose_name_plural = 'Product Unit'

    def __str__(self):
        return self.packing_type


class Product(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    packing = models.ForeignKey(Packing, on_delete=models.DO_NOTHING, blank=True, null=True)
    unit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    packing_extra = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    origin = models.ForeignKey(Origin, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name


class Warehouse(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    warehouse_name = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.warehouse_name





