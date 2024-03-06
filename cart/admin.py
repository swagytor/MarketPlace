from django.contrib import admin

from cart.models import UserCart, Cart


# Register your models here.
@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    ordering = ('id', 'cart', 'product', 'quantity')
    search_fields = ('product__title', 'cart__user__username')


class ProductInline(admin.TabularInline):
    model = UserCart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    ordering = ('user',)
    search_fields = ('user__username',)
    inlines = [ProductInline]
