from django.db import models
from django.utils import timezone
from django.db.models import Sum
from datetime import date
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


class Package(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(f"{self.name}")

    class Meta:
        verbose_name_plural = "Package Set"


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(f"{self.name}")

    class Meta:
        verbose_name_plural = "Brand Set"


class UnitSet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(f"{self.name}")

    class Meta:
        verbose_name_plural = "Unit Set"


class UnitValue(models.Model):
    unit = models.ForeignKey(UnitSet, on_delete=models.DO_NOTHING, related_name="unit_fk")
    value = models.CharField(max_length=10)

    def __str__(self):
        return str(f"{self.value}")

    class Meta:
        verbose_name_plural = "Unit Value"


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, related_name="brand_fk")
    unit = models.ForeignKey(UnitSet, on_delete=models.DO_NOTHING, related_name="unit_fk2")
    value = models.ForeignKey(UnitValue, on_delete=models.DO_NOTHING, related_name="value_fk")
    package = models.ForeignKey(Package, on_delete=models.DO_NOTHING, related_name="package_fk")
    buy_price = models.FloatField(max_length=10)
    sell_price = models.FloatField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f"{self.name}")

    def available(self):
        try:
            stockin = PurchaseItem.objects.filter(product__id = self.id).aggregate(Sum('quantity'))
            stockin = stockin['quantity__sum']
        except:
            stockin = 0
        try:
            stockout = SellItem.objects.filter(product__id = self.id).aggregate(Sum('quantity'))
            stockout = stockout['quantity__sum']
        except:
            stockout = 0

        stockin = stockin if not stockin is None else 0
        stockout = stockout if not stockout is None else 0

        return float(stockin - stockout)

    def stock_value(self):
        value = self.available() * self.buy_price
        return value

    class Meta:
        verbose_name_plural = "Product Set"


class PurchaseSet(models.Model):
    code = models.CharField(max_length=100)
    status = models.CharField(max_length=3,
                              choices=(('0', 'Pending'), ('1', 'In-progress'), ('2', 'Done')),
                              default=0)
    total_amount = models.FloatField(max_length=10)
    paid = models.FloatField(max_length=10)
    due = models.FloatField(max_length=10)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.code}")

    class Meta:
        verbose_name_plural = "Purchase Set"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(PurchaseSet, on_delete=models.CASCADE, related_name="purchase_fk")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="product_fk")
    unit_value = models.CharField(max_length=10)
    price = models.FloatField(max_length=10)
    quantity = models.FloatField(max_length=10)
    total_amount = models.FloatField(max_length=10)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.purchase.code} - {self.product.name}")

    class Meta:
        verbose_name_plural = "Purchase Item"


class SellSet(models.Model):
    code = models.CharField(max_length=100)
    client = models.CharField(max_length=2,
                              choices=(('1', 'Resort'), ('2', 'Restaurant')),
                              default=1)
    status = models.CharField(max_length=3,
                              choices=(('0', 'Pending'), ('1', 'In-progress'), ('2', 'Done')),
                              default=0)
    total_amount = models.FloatField(max_length=10)
    paid = models.FloatField(max_length=10)
    due = models.FloatField(max_length=10)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.code}")

    def short(self):
        short = float(self.total_amount) - float(self.paid)
        return short

    class Meta:
        verbose_name_plural = "Sell Set"


class SellItem(models.Model):
    sell = models.ForeignKey(SellSet, on_delete=models.CASCADE, related_name="sell_fk")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="product_fk2")
    unit_value = models.CharField(max_length=10)
    price = models.FloatField(max_length=10)
    quantity = models.FloatField(max_length=10)
    total_amount = models.FloatField(max_length=10)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.sell.code} - {self.product.name}")

    class Meta:
        verbose_name_plural = "Sell Item"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile.jpeg', upload_to='profile-pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

