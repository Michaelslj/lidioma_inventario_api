# inventario/filters.py
import django_filters
from inventario.models import Categoria


class CategoriaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Categoria
        fields = ['activa']