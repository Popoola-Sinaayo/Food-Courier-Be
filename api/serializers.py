from .models import *

from rest_framework.serializers import ModelSerializer


class Custom_User_Serializer(ModelSerializer):
    class Meta:
        model = Custom_User
        fields = ['id', 'name', 'phone_number', 'country', 'avatar']


class Banner_Serializer(ModelSerializer):
    class Meta:
        model = Banners
        fields = ['id', 'images']


class Product_Serializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'quantity', 'price']


class Cart_Serializer(ModelSerializer):
    product = Product_Serializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_no']
