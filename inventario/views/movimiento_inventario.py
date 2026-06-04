# inventario/views/movimiento_inventario.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from inventario.models import MovimientoInventario
from inventario.serializers import SerializerMovimientoInventario
from inventario.filters import FiltroMovimientoInventario


class MovimientoInventarioViewSet(viewsets.ModelViewSet):

    queryset = MovimientoInventario.objects.select_related('producto', 'usuario').all()
    serializer_class = SerializerMovimientoInventario
    
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    filterset_class = FiltroMovimientoInventario
    
    ordering_fields = ['creado_en', 'cantidad']
    ordering = ['-creado_en'] 

    def get_queryset(self):

        return self.queryset