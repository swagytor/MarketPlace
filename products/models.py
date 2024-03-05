from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=150, unique=True, verbose_name='SLUG')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Родительская категория', related_name='subcategories')
    img = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return f"Подкатегория {self.title}" if self.category else f"Категория {self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.CharField(max_length=255, unique=True, verbose_name='SLUG')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    small_img = models.ImageField(upload_to='products/small/', null=True, blank=True, verbose_name='Малое изображение')
    img = models.ImageField(upload_to='products/medium', null=True, blank=True, verbose_name='Изображение')
    big_img = models.ImageField(upload_to='products/big/', null=True, blank=True, verbose_name='Большое изображение')

    def __str__(self):
        return f'{self.title} ({self.category.title})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
