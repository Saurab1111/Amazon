from django.shortcuts import render
from .models import Product,Order
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from .serializers import ProductSerializer,OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission

class AuthUser(BasePermission):
    def has_permission(self, request, view):
        if request.user_sub:
            return True
        else:
            return False

class ProductList(APIView):
    def get(self,request):
        objects=Product.objects.all()
        if objects:
            serializer= ProductSerializer(objects,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("No product Available in list")
    
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response("Invalid entry",status=status.HTTP_204_NO_CONTENT)

class ProductDetail(RetrieveUpdateDestroyAPIView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        print(slug,"slug")
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")
    serializer_class=ProductSerializer

class OrderList(ListCreateAPIView):
    # permission_classes=AuthUser #only logged in user can place order (But we are already validating)
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()  #must do else serializer don't have request and all if we override serializer context
        context['slug'] = self.request.query_params.get('slug')
        context['user_id'] = self.request.user_sub
        print(context['slug'])
        return context


class OrderDetails(RetrieveUpdateDestroyAPIView):
    try:
        def get_object(self):
            track_number=self.kwargs.get('track_number')
            return Order.objects.get(track_number=track_number)
    except Order.DoesNotExist:
        raise NotFound(detail='No such order')
    
    serializer_class=OrderSerializer

    