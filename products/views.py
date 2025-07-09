from django.shortcuts import render
from .models import Product
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

class ProductList(APIView):
    def get(self,request):
        objects=Product.objects.all()
        if objects:
            serializer= ProductSerializer(objects,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("No product Available")
    
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
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")
    serializer_class=ProductSerializer
