from datetime import datetime
from django import forms
from dataset import models
import datetime
from tabnanny import check
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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


class SaveShop(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = models.Shop
        fields = ('name',)

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                shop = models.Shop.objects.exclude(id=id).get(name=name)
            else:
                shop = models.Shop.objects.get(name=name)
        except:
            return name
        raise forms.ValidationError(f"Shop name {shop.name} already exist. Try other names.")


class SavePurchase(forms.ModelForm):
    code = forms.CharField(max_length=50)
    total_amount = forms.CharField(max_length=10)
    paid = forms.CharField(max_length=10)
    due = forms.CharField(max_length=10)
    status = forms.CharField(max_length=3)
    shop = forms.Select(
        attrs={'class': 'form-control form-control-sm', 'value': '', 'id': 'id_shop'}
    )

    class Meta:
        model = models.PurchaseSet
        fields = ('code', 'total_amount', 'paid', 'due', 'status', 'shop',)

    def clean_code(self):
        code = self.cleaned_data['code']

        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.PurchaseSet.objects.get(code=f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code

    def save(self):
        instance = self.instance
        Products = []
        Payments = []

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

        if 'pay_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('pay_id[]')):
                pay = models.Pay.objects.get(id=val)
                note = self.data.getlist('pay_note[]')[k]
                price = self.data.getlist('pay_price[]')[k]
                date = self.data.getlist('pay_date[]')[k]
                total = float(price)

                try:
                    Payments.append(models.PurchasePayment(purchase=instance, pay=pay, note=note, amount=price, date=date, total_amount=total))
                    print("Purchase Payments..")
                except Exception as err:
                    print(err)
                    return False

        try:
            instance.save()
            models.PurchaseItem.objects.filter(purchase=instance).delete()
            models.PurchaseItem.objects.bulk_create(Products)
            models.PurchasePayment.objects.filter(purchase=instance).delete()
            models.PurchasePayment.objects.bulk_create(Payments)
        except Exception as err:
            print(err)
            return False


class SavePayment(forms.ModelForm):
    code = forms.CharField(max_length=50)
    total_amount = forms.CharField(max_length=10)

    class Meta:
        model = models.PaymentSet
        fields = ('code', 'total_amount',)

    def clean_code(self):
        code = self.cleaned_data['code']

        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.PaymentSet.objects.get(code=f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code

    def save(self):
        instance = self.instance
        Payments = []

        if 'shop_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('shop_id[]')):
                shop = models.Shop.objects.get(id=val)
                note = self.data.getlist('shop_note[]')[k]
                price = self.data.getlist('shop_price[]')[k]
                date = self.data.getlist('shop_date[]')[k]
                total = float(price)

                try:
                    Payments.append(models.PaymentItem(payment=instance, shop=shop, note=note, amount=price, date=date, total_amount=total))
                    print("PaymentsItems..")
                except Exception as err:
                    print(err)
                    return False

        try:
            instance.save()
            models.PaymentItem.objects.filter(payment=instance).delete()
            models.PaymentItem.objects.bulk_create(Payments)
        except Exception as err:
            print(err)
            return False


class SaveClient(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = models.Client
        fields = ('name',)

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                client = models.Client.objects.exclude(id=id).get(name=name)
            else:
                client = models.Client.objects.get(name=name)
        except:
            return name
        raise forms.ValidationError(f"Client name {client.name} already exist. Try other names.")


class SaveSell(forms.ModelForm):
    code = forms.CharField(max_length=50)
    client = forms.Select(
        attrs={'class': 'form-control form-control-sm', 'value': '', 'id': 'id_client'}
    )
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
                    check = models.SellSet.objects.get(code=f"{pref}{code:05d}")
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


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['image']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),

        }


class UpdateUser(UserChangeForm):
    email = forms.EmailField(max_length=100, required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
