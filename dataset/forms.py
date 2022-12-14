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
        raise forms.ValidationError(f"Brand {brand.name} already exist.")