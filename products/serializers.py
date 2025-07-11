from rest_framework import serializers
from .models import Product,Order
from datetime import datetime
class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        fields='__all__'
        model=Product

class OrderSerializer(serializers.ModelSerializer):
    product=serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        lookup_field='slug',
        read_only=True
    )
    user_id = serializers.CharField(read_only=True)
    track_number = serializers.IntegerField(read_only=True)
    class Meta:
        fields='__all__'
        model=Order
    
    def create(self,validated_data):
        product=Product.objects.get(slug=self.context['slug'])
        if product.quantity_available>0:
            validated_data['user_id']=self.context['user_id']
            validated_data['product']=product
            now = datetime.now()
            track_number=now.strftime("%d%m%Y%H%M%S")
            validated_data['track_number']=int(track_number)
            order = Order.objects.create(**validated_data)
            product.quantity_available-=1   #must return because object created but needs to return to view to return it in response.
            return order
        else:
            raise serializers.ValidationError("Not enough stock.")
    