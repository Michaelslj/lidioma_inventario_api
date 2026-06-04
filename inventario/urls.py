# inventario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from inventario.views.health import health_check
from inventario.views.auth import RegisterView, LogoutView
from inventario.views.user import UserViewSet
from inventario.views.categoria import CategoriaViewSet
from inventario.views.product import ConjuntoVistasProducto
from inventario.views.movimiento_inventario import MovimientoInventarioViewSet 
from inventario.serializers.auth import CustomTokenView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('productos', ConjuntoVistasProducto, basename='producto')
router.register('movimientos', MovimientoInventarioViewSet, basename='movimiento-inventario')  

urlpatterns = [
    path('health/', health_check),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/', TokenVerifyView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('', include(router.urls)),
]