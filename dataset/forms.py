from datetime import datetime
from django import forms
from dataset import models
import datetime
from tabnanny import check


class SaveBrand(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = models.Brand
        fields = ('name',)

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                brand = models.Brand.objects.exclude(id=id).get(name=name)
            else:
                brand = models.Brand.objects.get(name=name)
        except:
            return name
        raise forms.ValidationError(f"Brand {brand.name} already exist. Try other names.")


class SavePackage(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = models.Package
        fields = ('name',)

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                package = models.Package.objects.exclude(id=id).get(name=name)
            else:
                package = models.Package.objects.get(name=name)
        except:
            return name
        raise forms.ValidationError(f"Package {package.name} already exist. Try other names.")


class SaveUnitSet(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = models.UnitSet
        fields = ('name',)

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                unit_set = models.UnitSet.objects.exclude(id=id).get(name=name)
            else:
                unit_set = models.UnitSet.objects.get(name=name)
        except:
            return name
        raise forms.ValidationError(f"Unit Set {unit_set.name} already exist. Try other names.")


class SaveUnitValue(forms.ModelForm):
    unit = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_unit'}
    )
    value = forms.CharField(max_length=10)

    class Meta:
        model = models.UnitValue
        fields = ('unit', 'value',)

    def clean_value(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        value = self.cleaned_data['value']
        try:
            if id > 0:
                unit_value = models.UnitValue.objects.exclude(id=id).get(value=value)
            else:
                unit_value = models.UnitValue.objects.get(value=value)
        except:
            return value
        raise forms.ValidationError(f"Unit value {unit_value.value} already exist. Try other values.")


class SaveProduct(forms.ModelForm):
    name = forms.CharField(max_length=100)
    code = forms.CharField(max_length=100)
    brand = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_brand'}
    )
    unit = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_unit'}
    )
    value = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_value'}
    )
    package = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_package'}
    )
    buy_price = forms.CharField(max_length=10)
    sell_price = forms.CharField(max_length=10)

    class Meta:
        model = models.Product
        fields = ('name', 'code', 'brand', 'unit', 'value', 'package', 'buy_price', 'sell_price',)

    def clean_code(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        code = self.cleaned_data['code']
        try:
            if id > 0:
                product = models.Product.objects.exclude(id=id).get(code=code)
            else:
                product = models.Product.objects.get(code=code)
        except:
            return code
        raise forms.ValidationError(f"Product code {product.code} already exist. Try other codes.")


class SavePurchase(forms.ModelForm):
    code = forms.CharField(max_length=50)
    total_amount = forms.CharField(max_length=10)
    paid = forms.CharField(max_length=10)
    due = forms.CharField(max_length=10)
    status = forms.CharField(max_length=3)

    class Meta:
        model = models.PurchaseSet
        fields = ('code', 'total_amount', 'paid', 'due', 'status',)

    def clean_code(self):
        code = self.cleaned_data['code']

        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.PurchaseSet.objects.get(code=f"{pref}{code:03d}")
                    code = code + 1
                except:
                    return f"{pref}{code:03d}"
                    break
        else:
            return code

    def save(self):
        instance = self.instance
        Products = []

        if 'product_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('product_id[]')):
                product = models.Product.objects.get(id=val)
                unit = self.data.getlist('product_unit[]')[k]
                price = self.data.getlist('product_price[]')[k]
                qty = self.data.getlist('product_quantity[]')[k]
                total = float(price) * float(qty)

                try:
                    Products.append(models.PurchaseItem(purchase=instance, product=product, unit_value=unit, price=price, quantity=qty, total_amount=total))
                    print("Purchase Products..")
                except Exception as err:
                    print(err)
                    return False

        try:
            instance.save()
            models.PurchaseItem.objects.filter(purchase=instance).delete()
            models.PurchaseItem.objects.bulk_create(Products)
        except Exception as err:
            print(err)
            return False


class SaveSale(forms.ModelForm):
    code = forms.CharField(max_length=50)
    client = forms.CharField(max_length=2)
    status = forms.CharField(max_length=3)
    total_amount = forms.CharField(max_length=10)
    paid = forms.CharField(max_length=10)
    due = forms.CharField(max_length=10)

    class Meta:
        model = models.SellSet
        fields = ('code', 'client', 'status', 'total_amount', 'paid', 'due',)

    def clean_code(self):
        code = self.cleaned_data['code']

        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.SellSet.objects.get(code=f"{pref}{code:03d}")
                    code = code + 1
                except:
                    return f"{pref}{code:02}"
                    break
        else:
            return code

    def save(self):
        instance = self.instance
        Products = []

        if 'product_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('product_id[]')):
                product = models.Product.objects.get(id=val)
                unit = self.data.getlist('product_unit[]')[k]
                price = self.data.getlist('product_price[]')[k]
                qty = self.data.getlist('product_quantity[]')[k]
                total = float(price) * float(qty)

                try:
                    Products.append(models.SellItem(sell=instance, product=product, unit_value=unit, price=price, quantity=qty, total_amount=total))
                    print("Sell Items..")
                except Exception as err:
                    print(err)
                    return False

        try:
            instance.save()
            models.SellItem.objects.filter(sell=instance).delete()
            models.SellItem.objects.bulk_create(Products)
        except Exception as err:
            print(err)
            return False
