from modelos.producto import Producto
from modelos.cliente import Cliente
from modelos.venta import Venta


class Restaurante:
    """
    Servicio encargado de administrar las colecciones de productos, clientes y ventas, junto con las operaciones de registro, busqueda, 
    actualizacion, eliminacion, listado y venta del sistema. 
    PRINCIPIO SRP: maneja exclusivamente la logica de almacenamiento y validacion en memoria, cumpliendo con la restriccion de NO interactuar 
    con la consola (sin inputs ni prints) y de NO leer/escribir archivos directamente (eso es responsabilidad de ArchivoServicio).

    MEJORA SEMANA 11: se agrega self._ventas, una tercera coleccion que representa la relacion real entre un Cliente (Usuario) y un 
    Producto vendido, ademas de la operacion vender_producto() y la consulta de ventas por cliente.
    """

    def __init__(
        self,
        productos_iniciales: list[Producto] | None = None,
        clientes_iniciales: list[Cliente] | None = None,
        ventas_iniciales: list[Venta] | None = None,
    ) -> None:
        # LISTA (list):
        # self._productos guarda de manera conjunta Producto y su subclase Bebida (gracias al polimorfismo). self._clientes guarda 
        # objetos Cliente, que en este proyecto cumplen el rol de "Usuario" que se relaciona con Producto mediante Venta. self._ventas 
        # guarda la coleccion de relaciones ya concretadas (MEJORA SEMANA 11). Las tres listas son privadas: main.py nunca las recorre 
        # ni las modifica directamente, solo a traves de los metodos publicos de esta clase.
        self._productos: list[Producto] = (
            productos_iniciales.copy() if productos_iniciales else []
        )
        self._clientes: list[Cliente] = (
            clientes_iniciales.copy() if clientes_iniciales else []
        )
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []

    # -----------------------------------------------------------------
    # PRODUCTOS
    # -----------------------------------------------------------------
    def cargar_productos(self, productos: list[Producto]) -> None:
        """
        Reemplaza la coleccion en memoria por los productos recuperados desde datos/productos.json (ya convertidos a objetos 
        Producto/Bebida por ArchivoServicio). Se utiliza al iniciar main.py, antes de mostrar el menu.
        """
        self._productos = productos.copy()

    def registrar_producto(self, producto: Producto) -> str:
        """
        Registro de productos y evitar codigos de productos duplicados. Uso de LISTA: agrega el nuevo producto mediante 
        list.append().
        """
        if self.buscar_producto_por_codigo(producto.codigo) is not None:
            return f"Error: Ya existe un producto con el codigo {producto.codigo}."
        self._productos.append(producto)
        return f'El producto "{producto.nombre}" fue registrado exitosamente.'

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        """
        Implementa la busqueda de productos utilizando un criterio coherente como su codigo. Uso de LISTA: recorre self._productos 
        con un for para localizar el elemento buscado.
        """
        codigo = codigo.strip()
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str | None = None,
        categoria: str | None = None,
        precio: float | None = None,
        stock: int | None = None,
    ) -> str:
        """
        Implementa la actualizacion de productos. Localiza el producto dentro de la LISTA self._productos (a traves de 
        buscar_producto_por_codigo) y modifica sus atributos mediante los setters expuestos por Producto (que conservan sus 
        validaciones, incluida la del stock desde la Semana 11).
        """
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            return f"Error: No existe un producto con el codigo {codigo}."
        if nombre:
            producto.nombre = nombre
        if categoria:
            producto.categoria = categoria
        if precio is not None:
            producto.precio = precio
        if stock is not None:
            producto.stock = stock
        return f'El producto "{producto.codigo}" fue actualizado exitosamente.'

    def eliminar_producto(self, codigo: str) -> str:
        """
        Implementa la eliminacion de productos. Uso de LISTA: elimina el elemento localizado mediante list.remove().
        """
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            return f"Error: No existe un producto con el codigo {codigo}."
        self._productos.remove(producto)
        return f'El producto "{codigo}" fue eliminado exitosamente.'

    def listar_productos(self) -> list[str]:
        """
        Implementa el listado de productos. Uso de LISTA: recorre self._productos con comprension de lista.
        PRINCIPIO LSP & POLIMORFISMO: invoca mostrar_informacion() de forma transparente para Productos
        y Bebidas, sin usar isinstance().
        """
        return [producto.mostrar_informacion() for producto in self._productos]

    def obtener_productos(self) -> list[Producto]:
        """
        Entrega una copia de la coleccion de objetos Producto (no diccionarios) para que ArchivoServicio
        pueda convertirla a JSON y guardarla. Se devuelve una copia para que quien llama no pueda alterar
        la lista interna directamente (se respeta el encapsulamiento).
        """
        return self._productos.copy()

    def contar_productos(self) -> int:
        return len(self._productos)

    def obtener_categorias_unicas(self) -> set[str]:
        """
        CONJUNTO (set): se utiliza para obtener informacion que debe mostrarse sin elementos duplicados,
        por ejemplo las categorias unicas de los productos registrados.
        """
        categorias: set[str] = set()
        for producto in self._productos:
            categorias.add(producto.categoria)
        return categorias

    # -----------------------------------------------------------------
    # CLIENTES (rol de "Usuario" en la relacion Usuario-Producto-Venta)
    # -----------------------------------------------------------------
    def cargar_clientes(self, clientes: list[Cliente]) -> None:
        """
        MEJORA SEMANA 11: restaura la coleccion de clientes recuperada desde usuarios.json
        al iniciar el programa, igual que ya se hacia con los productos.
        """
        self._clientes = clientes.copy()

    def registrar_cliente(self, cliente: Cliente) -> str:
        """
        Permite el registro de clientes y evita identificaciones duplicadas. Uso de LISTA: agrega el nuevo
        cliente mediante list.append().
        """
        if self.buscar_cliente_por_identificacion(cliente.identificacion) is not None:
            return (
                f"Error: Ya existe un cliente con la identificacion "
                f"{cliente.identificacion}."
            )
        self._clientes.append(cliente)
        return f'El cliente "{cliente.nombre}" fue registrado exitosamente.'

    def buscar_cliente_por_identificacion(self, identificacion: str) -> Cliente | None:
        # Uso de LISTA: recorre self._clientes con un for para localizar el cliente buscado.
        # Se hace publico (Semana 11) porque vender_producto() necesita validar que el
        # usuario que compra realmente exista.
        identificacion = identificacion.strip()
        for cliente in self._clientes:
            if cliente.identificacion == identificacion:
                return cliente
        return None

    def listar_clientes(self) -> list[str]:
        """
        Permite el listado de clientes. Uso de LISTA: recorre self._clientes con comprension de lista.
        """
        return [cliente.mostrar_informacion() for cliente in self._clientes]

    def obtener_clientes(self) -> list[Cliente]:
        """
        MEJORA SEMANA 11: entrega una copia de la coleccion de objetos Cliente para que
        ArchivoServicio pueda guardarla en usuarios.json.
        """
        return self._clientes.copy()

    # -----------------------------------------------------------------
    # VENTAS -- MEJORA SEMANA 11: relacion Usuario (Cliente) + Producto -> Venta
    # -----------------------------------------------------------------
    def cargar_ventas(self, ventas: list[Venta]) -> None:
        """Restaura la coleccion de ventas recuperada desde ventas.json al iniciar el programa."""
        self._ventas = ventas.copy()

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_cliente: str,
        cantidad: int,
    ) -> bool:
        """
        Operacion central de la Semana 11: relaciona a un Cliente (Usuario) con un Producto mediante una Venta, controla el stock 
        disponible y lo disminuye solo cuando la operacion es valida.

        Reglas de negocio verificadas antes de crear la relacion:
        - Que el cliente exista.
        - Que el producto exista.
        - Que la cantidad solicitada sea mayor que cero.
        - Que exista stock suficiente.
        """
        cliente = self.buscar_cliente_por_identificacion(identificacion_cliente)
        producto = self.buscar_producto_por_codigo(codigo_producto)

        if cliente is None or producto is None:
            return False
        if cantidad <= 0 or producto.stock < cantidad:
            return False

        # Aqui se crea la relacion Usuario -> Producto y se agrega a la coleccion de ventas.
        venta = Venta(cliente.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)

        # Y aqui se ve el cambio interno del producto: el stock disminuye solo si la venta
        # ya fue validada y registrada.
        producto.vender(cantidad)
        return True

    def consultar_ventas_cliente(self, identificacion_cliente: str) -> list[Venta]:
        """
        Consulta que demuestra el uso de colecciones para recorrer, comparar y filtrar objetos:
        retorna unicamente las ventas asociadas a un cliente (usuario) especifico.
        """
        identificacion_cliente = identificacion_cliente.strip()
        ventas_cliente: list[Venta] = []
        for venta in self._ventas:
            if venta.usuario_id == identificacion_cliente:
                ventas_cliente.append(venta)
        return ventas_cliente

    def listar_ventas(self) -> list[str]:
        return [str(venta) for venta in self._ventas]

    def obtener_ventas(self) -> list[Venta]:
        """
        MEJORA SEMANA 11: entrega una copia de la coleccion de objetos Venta para que ArchivoServicio pueda guardarla en ventas.json.
        """
        return self._ventas.copy()


