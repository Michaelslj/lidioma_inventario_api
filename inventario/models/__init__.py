# inventario/models/__init__.py
from .categoria import Categoria
from .producto import Producto 
from .movimiento_inventario import MovimientoInventario

__all__ = ['Categoria', 'Producto', 'MovimientoInventario']