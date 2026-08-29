import json
from pathlib import Path

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from modelos.venta import Venta

# Relaciona el campo "tipo" guardado en el JSON con la clase que debe reconstruirse. Si en el futuro se agrega un nuevo tipo de producto 
# (por ejemplo Postre), bastaria con registrar su clase aqui (principio OCP).
TIPOS_PRODUCTO: dict[str, type[Producto]] = {
    Producto.TIPO: Producto,
    Bebida.TIPO: Bebida,
}


class ArchivoServicio:
    """
    Servicio encargado de leer y guardar los datos del restaurante en formato JSON, utilizando with open(), json.load() y json.dump(). 
    No conoce nada sobre el menu ni sobre la logica de negocio del restaurante: su unica responsabilidad es la persistencia (SRP).

    MEJORA SEMANA 11: ademas de productos.json (ya existente desde la Semana 10), ahora centraliza tambien la persistencia de usuarios.json 
    (clientes) y ventas.json (relacion Usuario-Producto), todos dentro de una misma carpeta "datos".
    """

    def __init__(self, ruta_datos: str = "datos") -> None:
        self._ruta_datos = Path(ruta_datos)
        self._ruta_productos = self._ruta_datos / "productos.json"
        self._ruta_usuarios = self._ruta_datos / "usuarios.json"
        self._ruta_ventas = self._ruta_datos / "ventas.json"

    # -----------------------------------------------------------------
    # PRODUCTOS
    # -----------------------------------------------------------------
    def cargar_productos(self) -> list[Producto]:
        """
        Lee datos/productos.json y reconstruye la coleccion de objetos Producto (y Bebida, cuando corresponda). Controla de forma especifica 
        los problemas que puede presentar el archivo, sin detener la aplicacion.
        """
        datos = self._leer_lista(self._ruta_productos, "productos")
        productos: list[Producto] = []
        for registro in datos:
            if not isinstance(registro, dict):
                print(
                    "Se encontro un registro de producto con formato invalido "
                    "y fue omitido."
                )
                continue
            try:
                producto = self._reconstruir_producto(registro)
                productos.append(producto)
            except KeyError as error:
                print(
                    f"Se encontro un registro de producto incompleto "
                    f"(falta la clave {error}) y fue omitido."
                )
            except ValueError as error:
                print(f"Se encontro un producto con datos invalidos: {error}")
        return productos

    def guardar_productos(self, productos: list[Producto]) -> bool:
        """
        Convierte la coleccion de objetos Producto/Bebida a una lista de diccionarios (mediante convertir_a_diccionario(), que ahora incluye el 
        stock) y la guarda en datos/productos.json con json.dump().
        """
        datos = [producto.convertir_a_diccionario() for producto in productos]
        return self._guardar_lista(self._ruta_productos, datos, "productos")

    def _reconstruir_producto(self, registro: dict) -> Producto:
        """
        Reconstruye un objeto Producto o Bebida a partir de un registro leido desde JSON, usando el campo "tipo" para elegir la clase correcta. 
        Puede lanzar KeyError (clave faltante) o ValueError (dato invalido, propagado desde los setters de Producto/Bebida); ambas excepciones 
        son controladas por quien llama a este metodo (cargar_productos()).
        """
        tipo = registro.get("tipo", Producto.TIPO)
        clase_producto = TIPOS_PRODUCTO.get(tipo, Producto)
        stock = registro.get("stock", 0)
        if clase_producto is Bebida:
            return Bebida(
                registro["codigo"],
                registro["nombre"],
                registro["categoria"],
                registro["precio"],
                registro["tamano"],
                stock,
            )
        return Producto(
            registro["codigo"],
            registro["nombre"],
            registro["categoria"],
            registro["precio"],
            stock,
        )

    # -----------------------------------------------------------------
    # USUARIOS (CLIENTES) -- MEJORA SEMANA 11
    # -----------------------------------------------------------------
    def cargar_clientes(self) -> list[Cliente]:
        """
        MEJORA SEMANA 11: completa la persistencia de clientes, que en la Semana 10 solo se administraban en memoria. Lee usuarios.json y 
        reconstruye objetos Cliente.
        """
        datos = self._leer_lista(self._ruta_usuarios, "usuarios")
        clientes: list[Cliente] = []
        for registro in datos:
            if not isinstance(registro, dict):
                print(
                    "Se encontro un registro de usuario con formato invalido "
                    "y fue omitido."
                )
                continue
            try:
                clientes.append(
                    Cliente(
                        registro["identificacion"],
                        registro["nombre"],
                        registro["correo"],
                    )
                )
            except KeyError as error:
                print(
                    f"Se encontro un registro de usuario incompleto "
                    f"(falta la clave {error}) y fue omitido."
                )
            except ValueError as error:
                print(f"Se encontro un usuario con datos invalidos: {error}")
        return clientes

    def guardar_clientes(self, clientes: list[Cliente]) -> bool:
        # Objetos Cliente -> diccionarios -> usuarios.json.
        datos = [cliente.convertir_a_diccionario() for cliente in clientes]
        return self._guardar_lista(self._ruta_usuarios, datos, "usuarios")

    # -----------------------------------------------------------------
    # VENTAS -- MEJORA SEMANA 11
    # -----------------------------------------------------------------
    def cargar_ventas(self) -> list[Venta]:
        """
        MEJORA SEMANA 11: reconstruye las ventas ya realizadas para que, al reiniciar el programa, la consulta de ventas por usuario siga 
        funcionando sobre datos reales.
        """
        datos = self._leer_lista(self._ruta_ventas, "ventas")
        ventas: list[Venta] = []
        for registro in datos:
            if not isinstance(registro, dict):
                print(
                    "Se encontro un registro de venta con formato invalido "
                    "y fue omitido."
                )
                continue
            try:
                ventas.append(
                    Venta(
                        registro["usuario_id"],
                        registro["producto_codigo"],
                        registro["cantidad"],
                    )
                )
            except KeyError as error:
                print(
                    f"Se encontro un registro de venta incompleto "
                    f"(falta la clave {error}) y fue omitido."
                )
            except ValueError as error:
                print(f"Se encontro una venta con datos invalidos: {error}")
        return ventas

    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        # Objetos Venta -> diccionarios -> ventas.json.
        datos = [venta.convertir_a_diccionario() for venta in ventas]
        return self._guardar_lista(self._ruta_ventas, datos, "ventas")

    # -----------------------------------------------------------------
    # Metodos de apoyo compartidos (evitan repetir el manejo de excepciones)
    # -----------------------------------------------------------------
    def _leer_lista(self, ruta: Path, nombre: str) -> list:
        """
        Controla los problemas que puede presentar cualquiera de los tres archivos JSON, sin detener la aplicacion:
        - FileNotFoundError: el archivo todavia no existe (primer inicio) -> lista vacia.
        - json.JSONDecodeError: el contenido no es un JSON valido -> se informa y lista vacia.
        - PermissionError: no hay permisos suficientes para leer el archivo.
        """
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"El archivo de {nombre} no tiene un formato JSON valido.")
            return []
        except PermissionError:
            print(f"No hay permisos suficientes para leer el archivo de {nombre}.")
            return []

        if not isinstance(datos, list):
            print(f"El archivo de {nombre} debe contener una lista de registros.")
            return []
        return datos

    def _guardar_lista(self, ruta: Path, datos: list, nombre: str) -> bool:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"No hay permisos suficientes para guardar el archivo de {nombre}.")
            return False


