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
    unit_set = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_unit_set'}
    )
    unit_value = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_unit_value'}
    )
    package = forms.Select(
        attrs={'class': 'form-control form-control-sm rounded-0', 'value': '', 'id': 'id_package'}
    )
    buy_price = forms.CharField(max_length=10)
    sell_price = forms.CharField(max_length=10)

    class Meta:
        models = models.Product
        fields = ('name', 'code', 'brand', 'unit_set', 'unit_value', 'package', 'buy_price', 'sell_price',)

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