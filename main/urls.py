from django.urls import path

from main.views import ProductMaterialsView

urlpatterns = [
    path('product/', ProductMaterialsView.as_view(), name='product')
]