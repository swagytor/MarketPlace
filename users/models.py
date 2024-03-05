from django.contrib.auth.models import AbstractUser, User
from django.db import models

from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class UserCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
