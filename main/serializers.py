from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import IntegerField
from .models import Product, ProductMaterial, Material, Warehouses


class ProductModelSerializer(ModelSerializer):
    count = IntegerField(min_value=0, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class MaterialModelSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class ProductmaterialModelSerializer(ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = "__all__"


class WarehousesModelSerializer(ModelSerializer):
    class Meta:
        model = Warehouses
        fields = "__all__"
