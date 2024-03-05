import os

from PIL import Image
from django.shortcuts import render
from pytils.translit import slugify
from rest_framework import viewsets

from MarketPlace.settings import BASE_DIR
from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer, CategoryListSerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
