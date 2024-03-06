from django.db import models
from pytils.translit import slugify

from products.service import resize_images


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='SLUG')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Родительская категория', related_name='subcategories')
    img = models.ImageField(upload_to='category/', null=True, blank=True, verbose_name='Изображение')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Подкатегория {self.title}" if self.category else f"Категория {self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='SLUG')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    small_img = models.ImageField(upload_to='product/small/', null=True, blank=True, verbose_name='Малое изображение')
    medium_img = models.ImageField(upload_to='product/medium', null=True, blank=True,
                                   verbose_name='Среднее изображение')
    img = models.ImageField(upload_to='product/big/', null=True, blank=True, verbose_name='Изображение')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
            self.save()

        if self.img:
            img_name = self.img.name.split('/')[-1]
            if not (self.small_img and self.medium_img):
                resize_images(self)
            elif ((self.small_img and self.medium_img) and
                  (not self.small_img.name.endswith(img_name) or not self.medium_img.name.endswith(img_name))):
                resize_images(self)

    def __str__(self):
        return f'{self.title} ({self.category.title})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
