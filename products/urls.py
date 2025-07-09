from django.urls import path
from .views import ProductDetail,ProductList


urlpatterns = [
    path('all-products/', ProductList.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetail.as_view(), name='product-detail'),
]
