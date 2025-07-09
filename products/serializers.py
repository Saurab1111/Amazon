from rest_framework import serializers
from .models import Product
from django.utils.text import slugify
class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        fields='__all__'
        model=Product
    