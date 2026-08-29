# Archivo requerido para identificar el paquete servicios. Crear los archivos __init__.py correspondientes en los paquetes es parte de 
# la buena practica de la POO. Este archivo identifica a servicios/ como paquete de Python, permitiendo las importaciones como 
# "from servicios.restaurante import Restaurante".

from .restaurante import Restaurante
from .archivo_servicio import ArchivoServicio

__all__ = ["Restaurante", "ArchivoServicio"]


