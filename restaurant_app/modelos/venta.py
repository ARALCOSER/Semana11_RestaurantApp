class Venta:
    """
    MEJORA SEMANA 11: nuevo modelo que representa la relacion entre un Usuario (en este proyecto,
    Cliente) y un Producto vendido. Una venta no es solo restar stock: tambien queda registrada como
    un objeto propio dentro de una coleccion (self._ventas en Restaurante), lo que permite luego
    recorrerla, compararla y filtrarla (por ejemplo, para consultar las ventas de un cliente).

    PRINCIPIO SRP: su unica responsabilidad es representar y validar los datos de la operacion de venta
    ya realizada (usuario_id, producto_codigo y cantidad). No conoce nada sobre el stock del producto,
    ni sobre como se guarda en ventas.json: eso lo resuelven Restaurante y ArchivoServicio.
    """

    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int) -> None:
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    @property
    def usuario_id(self) -> str:
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion del usuario no puede estar vacia.")
        self._usuario_id = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo del producto no puede estar vacio.")
        self._producto_codigo = valor.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        try:
            cantidad_convertida = int(valor)
        except (TypeError, ValueError):
            raise ValueError("La cantidad vendida debe ser un numero entero.")
        if cantidad_convertida <= 0:
            raise ValueError("La cantidad vendida debe ser mayor que cero.")
        self._cantidad = cantidad_convertida

    def convertir_a_diccionario(self) -> dict:
        """
        Permite que ArchivoServicio guarde la venta en ventas.json mediante json.dump(),
        conservando la relacion Usuario-Producto realizada.
        """
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    def __str__(self) -> str:
        return (
            f"Usuario: {self.usuario_id} | Producto: {self.producto_codigo} | "
            f"Cantidad: {self.cantidad}"
        )


