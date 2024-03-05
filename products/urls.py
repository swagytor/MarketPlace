from django.urls import path
from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = router.urls
