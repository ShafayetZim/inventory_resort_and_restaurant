from rest_framework import serializers

from sales.models import SalesChild
from ecommerce.models import Warehouse


class SalesItemSerializerPopUp(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.product_name', read_only=True)

    class Meta:
        model = SalesChild
        fields = '__all__'
