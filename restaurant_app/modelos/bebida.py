from modelos.producto import Producto


class Bebida(Producto):
    """
    Clase hija de Producto que incorpora informacion especifica de una bebida. Aplicacion estricta de
    herencia (Bebida ES-UN Producto). PRINCIPIO LSP: se puede usar un objeto Bebida en cualquier lugar
    donde se espere un Producto (por ejemplo, dentro de la misma lista de productos del servicio Restaurante,
    dentro del mismo archivo productos.json, o al momento de venderla con vender_producto()).
    """

    TIPO: str = "bebida"

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        tamano: str,
        stock: int = 0,
    ) -> None:
        # Reutilizacion del constructor de la clase base mediante super(), en lugar
        # de repetir la asignacion de atributos ya definidos en Producto (incluido el
        # nuevo atributo "stock" de la Semana 11).
        super().__init__(codigo, nombre, categoria, precio, stock)
        # Incorporacion de un atributo especifico (el tamaño) propio de la clase
        # hija, manteniendo el encapsulamiento con atributo protegido, propiedad y validacion.
        self.tamano = tamano

    @property
    def tamano(self) -> str:
        return self._tamano

    @tamano.setter
    def tamano(self, nuevo_tamano: str) -> None:
        if not nuevo_tamano or not nuevo_tamano.strip():
            raise ValueError("El tamano de la bebida no puede estar vacio.")
        self._tamano = nuevo_tamano.strip()

    def mostrar_informacion(self) -> str:
        """
        Sobrescribe el metodo aplicando POLIMORFISMO puro. Retorna la informacion especializada
        incluyendo el atributo propio de la clase hija (tamaño) y el stock heredado de Producto,
        sin que servicios/restaurante.py necesite preguntar isinstance() para saber que tipo de
        producto esta mostrando.
        """
        return (
            f"[Bebida] Codigo: {self.codigo} | Nombre: {self.nombre} | "
            f"Categoria: {self.categoria} | Precio: ${self.precio:.2f} | "
            f"Tamano: {self.tamano} | Stock: {self.stock}"
        )

    def convertir_a_diccionario(self) -> dict:
        """
        Extiende la conversion de la clase base (que ya incluye el stock) agregando el atributo
        "tamaño", propio de Bebida, para que no se pierda informacion al guardar en datos/productos.json.
        """
        datos = super().convertir_a_diccionario()
        datos["tamano"] = self.tamano
        return datos


