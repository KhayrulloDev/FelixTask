from rest_framework import generics
from rest_framework.response import Response
from collections import defaultdict
from django.db.models import FloatField, F, Sum, Value as V, ExpressionWrapper, Max
from django.db.models.functions import Coalesce
from .models import Warehouses
from .serializers import ProductModelSerializer
from .tests import check_and_adjust_remainders


class ProductMaterialsView(generics.GenericAPIView):
    serializer_class = ProductModelSerializer

    def get(self, request):
        products = [
            {'product': 'Koylak', 'qty': 30, 'materials': {'Mato': 24, 'Tugma': 150, 'Ip': 300}},
            {'product': 'Shim', 'qty': 20, 'materials': {'Mato': 28, 'Ip': 300, 'Zamok': 20}}
        ]

        remaining_materials = defaultdict(lambda: defaultdict(int))

        # Xomashyolar miqdori va narxlari
        warehouses = Warehouses.objects.values('material__name').annotate(
            total_quantity=Coalesce(Sum('remainder'), V(0), output_field=FloatField()),
            total_price=Coalesce(
                Sum(ExpressionWrapper(F('remainder') * F('price'), output_field=FloatField())), V(0),
                output_field=FloatField())
        )

        for warehouse in warehouses:
            remaining_materials[warehouse['material__name']]['qty'] = warehouse['total_quantity']
            remaining_materials[warehouse['material__name']]['price'] = warehouse['total_price']

        result = []

        for product_data in products:
            product_res = {
                "product_name": product_data['product'],
                "product_qty": product_data['qty'],
                "product_materials": []
            }

            for material_name, material_qty in product_data['materials'].items():
                material_res = []

                while material_qty > 0:
                    warehouse = Warehouses.objects.filter(material__name=material_name, remainder__gt=0).order_by('id').first()
                    if not warehouse:
                        break

                    required_qty = min(material_qty, warehouse.remainder)

                    material_res.append({
                        "warehouse_id": warehouse.id,
                        "material_name": warehouse.material.name,
                        "qty": required_qty,
                        "price": warehouse.price
                    })

                    remaining_materials[material_name]['qty'] -= required_qty
                    remaining_materials[material_name]['price'] -= required_qty * warehouse.price
                    warehouse.remainder -= required_qty
                    warehouse.save()

                    material_qty -= required_qty

                if material_qty > 0:
                    if not warehouse:
                        material_res.append({
                            "warehouse_id": None,
                            "material_name": material_name,
                            "qty": material_qty,
                            "price": None
                        })

                product_res["product_materials"].extend(material_res)

            result.append(product_res)

        return Response({"result": result}, check_and_adjust_remainders())


