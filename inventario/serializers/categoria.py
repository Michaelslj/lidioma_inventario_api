# inventario/serializers/categoria.py
from rest_framework import serializers
from django.utils.text import slugify
from inventario.models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    """
    El campo total_productos se agregará en la Etapa 4
    cuando el modelo Producto ya exista.
    Incluirlo antes provoca AttributeError.
    """

    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'slug', 'descripcion',
            'activa', 'creado_en',
        ]
        read_only_fields = ['id', 'creado_en']

    def validate_slug(self, value):
        return slugify(value)

    def validate_nombre(self, value):
        qs = Categoria.objects.filter(nombre__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Ya existe una categoría con este nombre.')
        return value