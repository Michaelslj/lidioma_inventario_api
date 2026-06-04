# inventario/serializers/movimiento_inventario.py
from rest_framework import serializers
from inventario.models import MovimientoInventario


class SerializerMovimientoInventario(serializers.ModelSerializer):
    # Definimos el usuario como de solo lectura para capturarlo automáticamente desde el request
    usuario = serializers.StringRelatedField(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = MovimientoInventario
        fields = [
            'id', 
            'producto', 
            'tipo', 
            'tipo_display', 
            'cantidad', 
            'motivo', 
            'usuario', 
            'creado_en'
        ]

    def validate(self, data):
        """
        Validación a nivel de serializador para capturar el ValueError 
        de stock insuficiente que programamos en el modelo y responder 
        con un HTTP 400 Bad Request limpio en Postman.
        """
        # Obtenemos el usuario autenticado desde el contexto de la petición
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            usuario_actual = request.user
        else:
            raise serializers.ValidationError(
                {"usuario": "Debe estar autenticado para realizar un movimiento de inventario."}
            )

        # Instanciamos un objeto temporal del modelo para simular la lógica del save()
        movimiento_temporal = MovimientoInventario(
            producto=data['producto'],
            tipo=data['tipo'],
            cantidad=data['cantidad'],
            motivo=data.get('motivo', ''),
            usuario=usuario_actual
        )

        try:
            # Simulamos el descuento/aumento de stock sin guardar todavía en la BD
            producto = movimiento_temporal.producto
            if movimiento_temporal.tipo in ['ENTRADA', 'AJUSTE_POS']:
                pass # Las entradas no generan problemas de stock negativo
            elif movimiento_temporal.tipo in ['SALIDA', 'AJUSTE_NEG']:
                if producto.stock < movimiento_temporal.cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {producto.nombre}. "
                        f"Disponible: {producto.stock}, Solicitado: {movimiento_temporal.cantidad}"
                    )
        except ValueError as e:
            raise serializers.ValidationError({"cantidad": str(e)})

        # Guardamos el usuario validado en el diccionario de datos limpios
        data['usuario'] = usuario_actual
        return data

    def create(self, validated_data):
        """
        Sobrescribimos el método de creación para inyectar el usuario 
        autenticado que guardamos en la validación.
        """
        return MovimientoInventario.objects.create(**validated_data)