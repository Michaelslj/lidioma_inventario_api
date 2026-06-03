# inventario/views/categoria.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from inventario.models import Categoria
from inventario.serializers.categoria import CategoriaSerializer
from inventario.permissions import EsStaffOSoloLectura
from inventario.filters import CategoriaFilter
from inventario.pagination import StandardPagination


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsStaffOSoloLectura]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CategoriaFilter
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'creado_en']
    ordering = ['nombre']

    @action(detail=True, methods=['get'], url_path='productos')
    def productos(self, request, pk=None):
        """
        Retorna lista vacía hasta la Etapa 4
        cuando se cree el modelo Producto.
        """
        return Response([])

    @action(detail=False, methods=['get'], url_path='estadisticas')
    def estadisticas(self, request):
        qs = Categoria.objects.annotate(num_productos=Count('products', distinct=True))

        return Response({
            'total': qs.count(),
            'activas': qs.filter(activa=True).count(),
            'inactivas': qs.filter(activa=False).count(),
            'detalle': [
                {
                    'id': c.id,
                    'nombre': c.nombre,
                    'num_productos': c.num_productos,
                    'activa': c.activa,
                }
                for c in qs.order_by('nombre')
            ],
        })