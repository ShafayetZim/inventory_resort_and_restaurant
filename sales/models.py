from django.contrib.auth.models import User
from django.db import models
import datetime
from ecommerce.models import Customers, Warehouse, Products


def invoice_no_generate():
    today_date = datetime.date.today()

    # GET Current Year
    current_year = today_date.strftime('%Y')
    prefix = "RR-" + current_year + "-"

    # For the very first time invoice_number is DD-MM-YY-0001
    next_invoice_no = '00001'

    # Get Last Employee Start With DNCC-MI-
    last_invoice_no = SalesParent.objects.filter(invoice_no__startswith=prefix).order_by('invoice_no').last()

    if last_invoice_no:
        # Cut 5 digit from the Right and converted to int (STC-YYYY-:xxxx)
        last_invoice_four_digit = int(last_invoice_no.invoice_no[-5:])

        # Increment one with last five digit
        next_invoice_no = '{0:05d}'.format(last_invoice_four_digit + 1)

    # Return custom invoice number
    return prefix + next_invoice_no


class SalesParent(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    order_date = models.DateField(blank=True, null=True)
    invoice_no = models.CharField(max_length=100, primary_key=True, default=invoice_no_generate)
    customer = models.ForeignKey(Customers, on_delete=models.DO_NOTHING, )
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, )
    quantity = models.DecimalField(max_digits=20, decimal_places=2, )
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    due_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, default="Open")
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice_no


class SalesChild(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    order_date = models.DateField(blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, )
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    packing_qty = models.DecimalField(max_digits=20, decimal_places=2, default=1)
    packing = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    packing_unit = models.CharField(max_length=20, blank=True, null=True)
    extra_field = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    invoice_no = models.ForeignKey(SalesParent, on_delete=models.DO_NOTHING, )
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice_no.invoice_no

    class Meta:
        unique_together = (('product', 'invoice_no'),)
