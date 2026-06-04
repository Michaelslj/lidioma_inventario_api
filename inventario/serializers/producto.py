# inventario/serializers/product.py
from rest_framework import serializers
from inventario.models import Producto
from inventario.serializers.categoria import CategoriaSerializer


class SerializerResumenProducto(serializers.ModelSerializer):

    class Meta:
        model  = Producto
        fields = ['id', 'codigo_barras', 'nombre', 'precio', 'stock', 'es_activo']


class SerializerProducto(serializers.ModelSerializer):
    categoria       = CategoriaSerializer(read_only=True)
    categoria_id    = serializers.PrimaryKeyRelatedField(
        source='categoria',
        write_only=True,
        queryset=Producto.objects.none(),
    )
    precio_con_impuesto = serializers.SerializerMethodField()
    en_stock       = serializers.SerializerMethodField()

    class Meta:
        model  = Producto
        fields = [
            'id', 'codigo_barras', 'nombre', 'descripcion',
            'precio', 'precio_con_impuesto',
            'stock', 'stock_minimo', 'en_stock', 'es_activo',
            'categoria', 'categoria_id',
            'creado_en', 'actualizado_en',
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from inventario.models import Categoria
        self.fields['categoria_id'].queryset = Categoria.objects.filter(is_active=True)

    def get_precio_con_impuesto(self, obj):
        return obj.precio_con_impuesto

    def get_en_stock(self, obj):
        return obj.en_stock

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor que 0.')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value