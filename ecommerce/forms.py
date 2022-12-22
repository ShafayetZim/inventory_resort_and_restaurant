from datetime import datetime
from django import forms
from ecommerce import models
import datetime
from tabnanny import check


class SaveBrand(forms.ModelForm):
    name = forms.CharField(max_length=250)

    class Meta:
        model = models.Brand
        fields = ('name',)

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                brand = models.Brand.objects.exclude(id=id).get(name=name, delete_flag=0)
            else:
                brand = models.Brand.objects.get(name=name, delete_flag=0)
        except:
            return name
        raise forms.ValidationError(f"Brand {brand.name} already exist")


class SaveProducts(forms.ModelForm):
    name = forms.CharField(max_length=250)
    code = forms.CharField(max_length=250)
    brand = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_brand'}
    )
    description = forms.CharField(max_length=250, required=False)
    buy = forms.CharField(max_length=250)
    price = forms.CharField(max_length=250)
    mrp = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Products
        fields = ('name', 'code', 'description', 'brand', 'buy', 'price', 'mrp', 'status', )

    def clean_code(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        code = self.cleaned_data['code']
        try:
            if id > 0:
                product = models.Products.objects.exclude(id = id).get(code = code, delete_flag = 0)
            else:
                product = models.Products.objects.get(code = code, delete_flag = 0)
        except:
            return code
        raise forms.ValidationError("Product code already exists.")


class SavePurchase(forms.ModelForm):
    code = forms.CharField(max_length=250)
    note = forms.CharField(max_length=250, required=False)
    brand = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_brand'}
    )
    status = forms.CharField(max_length=2)
    payment = forms.CharField(max_length=2)
    total_amount = forms.CharField(max_length=250)

    class Meta:
        model = models.Purchase
        fields = ('code', 'brand', 'status', 'payment', 'total_amount', )

    def clean_code(self):
        code = self.cleaned_data['code']

        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.Purchase.objects.get(code=f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code

    def save(self):
        instance = self.instance
        Products = []

        if 'product_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('product_id[]')):
                product = models.Products.objects.get(id=val)
                buy = self.data.getlist('product_price[]')[k]
                qty = self.data.getlist('product_quantity[]')[k]
                freeqty = self.data.getlist('product_free_quantity[]')[k]
                total = float(buy) * float(qty)

                try:
                    Products.append(models.PurchaseProducts(purchase=instance, product=product, buy=buy, quantity=qty, total_amount=total, free_quantity=freeqty))
                    print("SaleProducts..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.PurchaseProducts.objects.filter(purchase=instance).delete()
            models.PurchaseProducts.objects.bulk_create(Products)

        except Exception as err:
            print(err)
            return False