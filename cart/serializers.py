from django.db.models import Sum, F
from rest_framework import serializers

from cart.models import Cart, UserCart


class CartSerializer(serializers.ModelSerializer):
    _user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class MyCartSerializer(serializers.ModelSerializer):
    _product = serializers.SlugRelatedField(slug_field='title', read_only=True, source='product')

    class Meta:
        model = UserCart
        fields = '__all__'
        read_only_fields = ['cart']


class SummaryPriceSerializer(serializers.Serializer):
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    def get_total_quantity(self, instance):
        request = self.context.get('request')
        queryset = Cart.objects.filter(user=request.user)
        total_quantity = queryset.aggregate(total_quantity=Sum('usercart__quantity'))['total_quantity']
        return total_quantity

    def get_total_price(self, instance):
        request = self.context.get('request')
        queryset = Cart.objects.filter(user=request.user)
        total_price = queryset.annotate(
            product_total_price=F('usercart__product__price') * F('usercart__quantity')
        ).aggregate(total_price=Sum('product_total_price'))['total_price']
        return total_price

    class Meta:
        model = UserCart
        fields = '__all__'
