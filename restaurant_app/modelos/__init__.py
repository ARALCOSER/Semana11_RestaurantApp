# Archivo requerido para identificar el paquete modelos. Crear los archivos __init__.py correspondientes
# en los paquetes es parte de la buena practica de la POO. Este archivo identifica a modelos/ como paquete
# de Python, permitiendo las importaciones como "from modelos.producto import Producto".
#
# MEJORA SEMANA 11: se agrega Venta, el nuevo modelo que representa la relacion Usuario (Cliente) + Producto.
from .producto import Producto
from .bebida import Bebida
from .cliente import Cliente
from .venta import Venta

__all__ = ["Producto", "Bebida", "Cliente", "Venta"]


