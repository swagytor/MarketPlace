from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins

from cart.models import UserCart, Cart
from products.models import Product
from cart.serializers import MyCartSerializer, SummaryPriceSerializer


# Create your views here.
class MyCartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = UserCart.objects.all()
    serializer_class = MyCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCart.objects.filter(cart__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'total':
            return SummaryPriceSerializer
        return MyCartSerializer

    @action(methods=['get'], detail=False)
    def total(self, request):
        try:
            print(request.user)
            cart = Cart.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response({'detail': 'Корзина пуста'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer_class()
        serializer = serializer(instance=cart, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def add_to_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'detail': 'Нет такого продукта'}, status=status.HTTP_404_NOT_FOUND)

        product_cart, created = UserCart.objects.get_or_create(cart=cart, product=product)

        product_cart.quantity += quantity
        product_cart.save()

        return Response({'details:': f'Продукт {product.title} добавлен в корзину в количестве {quantity} шт.'},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def remove_from_cart(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response({'detail': 'Вы ещё ничего не добавили в корзину'}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'detail': 'Нет такого продукта'}, status=status.HTTP_404_NOT_FOUND)

        try:
            product_cart = UserCart.objects.get(cart=cart, product=product)
        except ObjectDoesNotExist:
            return Response({'detail': 'Такого продукта нет в корзине'}, status=status.HTTP_404_NOT_FOUND)

        if product_cart.quantity - quantity < 0:
            return Response({'detail': f'Нельзя уменьшить количество больше чем есть в корзине. '
                                       f'В корзине только {product_cart.quantity} шт. данного товара'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif product_cart.quantity - quantity == 0:
            product_cart.delete()
            return Response({'details:': f'Продукт {product.title} удален из корзины.'}, status=status.HTTP_200_OK)
        else:
            product_cart.quantity -= quantity
            product_cart.save()

        return Response(
            {'details:': f'Продукт {product.title} удален из корзины. Осталось {product_cart.quantity} шт.'},
            status=status.HTTP_200_OK)

    @extend_schema(request=None, responses=None)
    @action(methods=['post'], detail=False)
    def clear_cart(self, request):
        cart = self.get_queryset().get(cart__user=request.user)
        cart.delete()
        return Response({'details:': 'Корзина очищена'}, status=status.HTTP_200_OK)
