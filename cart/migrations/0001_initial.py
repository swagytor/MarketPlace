# Generated by Django 5.0.3 on 2024-03-06 06:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('products', '0004_alter_category_img_alter_product_img_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart', verbose_name='Корзина')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Продукт в корзине',
                'verbose_name_plural': 'Продукты в корзинах',
            },
        ),
    ]