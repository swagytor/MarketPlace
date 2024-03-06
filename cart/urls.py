from rest_framework.routers import DefaultRouter

from cart.views import MyCartViewSet

router = DefaultRouter()
router.register('', MyCartViewSet, basename='my_cart')

urlpatterns = router.urls
