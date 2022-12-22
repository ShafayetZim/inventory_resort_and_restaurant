from django.db import models
from django.utils import timezone
from django.db.models import Sum
from datetime import date


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
