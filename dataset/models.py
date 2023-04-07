from django.db import models
from django.utils import timezone
from django.db.models import Sum, Max
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

    @property
    def last_purchase_price(self):
        last_purchase_item = self.product_fk.all().order_by('-date', '-id').first()
        if last_purchase_item:
            return last_purchase_item.price
        else:
            return 0.0

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
        value = self.available() * self.last_purchase_price
        return value

    class Meta:
        verbose_name_plural = "Product Set"


class Shop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(f"{self.name}")

    def due(self):
        try:
            purchase = PurchaseSet.objects.filter(shop__id=self.id, status=0).aggregate(Sum('total_amount'))
            purchase = purchase['total_amount__sum']
        except:
            purchase = 0
        try:
            discount = PurchaseSet.objects.filter(shop__id=self.id, status=0).aggregate(Sum('paid'))
            discount = discount['paid__sum']
        except:
            discount = 0
        try:
            paid = PaymentItem.objects.filter(shop__id=self.id).aggregate(Sum('total_amount'))
            paid = paid['total_amount__sum']
        except:
            paid = 0

        purchase = purchase if not purchase is None else 0
        discount = discount if not discount is None else 0
        paid = paid if not paid is None else 0

        return float(purchase - discount - paid)

    class Meta:
        verbose_name_plural = "Shop"


class Pay(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(f"{self.name}")

    class Meta:
        verbose_name_plural = "Pay Due"


class PaymentSet(models.Model):
    code = models.CharField(max_length=100)
    total_amount = models.FloatField(max_length=10)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.code}")

    class Meta:
        verbose_name_plural = "Payment Set"


class PaymentItem(models.Model):
    payment = models.ForeignKey(PaymentSet, on_delete=models.CASCADE, related_name="payment_fk")
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, related_name="shop_fk2")
    note = models.CharField(max_length=250, blank=True, null=True)
    amount = models.FloatField(max_length=10)
    total_amount = models.FloatField(max_length=10)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.payment.code} - {self.shop.name}")

    class Meta:
        verbose_name_plural = "Payment Item"


class PurchaseSet(models.Model):
    code = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, null=True, related_name='shop_fk')
    status = models.CharField(max_length=3,
                              choices=(('0', 'Due'), ('1', 'Paid')),
                              default=0)
    image = models.ImageField(null=True, upload_to='voucher')
    total_amount = models.FloatField(max_length=10)
    discount = models.FloatField(max_length=10)
    cost = models.FloatField(max_length=10)
    net = models.FloatField(max_length=10)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.code}")

    def product_total(self):
        try:
            items = PurchaseItem.objects.filter(purchase=self).aggregate(Sum('total_amount'))
            items = items['total_amount__sum']
        except:
            items = 0
        return float(items)

    def payment_total(self):
        try:
            deposits = PurchasePayment.objects.filter(purchase=self).aggregate(Sum('total_amount'))
            deposits = deposits['total_amount__sum']
        except:
            deposits = 0
        return float(deposits)

    class Meta:
        verbose_name_plural = "Purchase Set"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(PurchaseSet, on_delete=models.CASCADE, related_name="purchase_fk")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="product_fk", null=True)
    note = models.CharField(max_length=250, blank=True, null=True)
    unit_value = models.CharField(max_length=10)
    price = models.FloatField(max_length=10)
    quantity = models.FloatField(max_length=10)
    total_amount = models.FloatField(max_length=10)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.purchase.code}")

    class Meta:
        verbose_name_plural = "Purchase Item"


class PurchasePayment(models.Model):
    purchase = models.ForeignKey(PurchaseSet, on_delete=models.CASCADE, related_name="purchase_fk2")
    pay = models.ForeignKey(Pay, on_delete=models.DO_NOTHING, related_name="pay_fk")
    note = models.CharField(max_length=250, blank=True, null=True)
    amount = models.FloatField(max_length=10)
    total_amount = models.FloatField(max_length=10)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.purchase.code} - {self.pay.name}")

    class Meta:
        verbose_name_plural = "Purchase Payment"


class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(f"{self.name}")

    class Meta:
        verbose_name_plural = "Client"


class SellSet(models.Model):
    code = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, related_name='client_fk')
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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="product_fk2", null=True)
    unit_value = models.CharField(max_length=10)
    price = models.FloatField(max_length=10)
    quantity = models.FloatField(max_length=10)
    total_amount = models.FloatField(max_length=10)
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(f"{self.sell.code}")

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


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userpreferences')
    receive_notifications = models.BooleanField(default=False)
    enable_dark_mode = models.BooleanField(default=False)
    hide_sensitive_content = models.BooleanField(default=False)
    # add more boolean fields as needed

    def __str__(self):
        return f"{self.user.username}'s preferences"

