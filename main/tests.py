from django.test import TestCase

from .models import Warehouses

def check_and_adjust_remainders():
    warehouse_remainders = {
        1: 12,
        2: 200,
        3: 40,
        4: 300,
        5: 500,
        6: 1000
    }

    for warehouse_id, remainder in warehouse_remainders.items():
        warehouse = Warehouses.objects.filter(id=warehouse_id).first()
        if warehouse and warehouse.remainder < remainder:
            warehouse.remainder = remainder
            warehouse.save()
