class Producto:
    """
    Clase base que representa un producto general del restaurante. Define los atributos obligatorios de
    Producto (codigo, nombre, categoria, precio y stock) y expone metodos para acceder y modificar dichos
    atributos de forma controlada.
    PRINCIPIO SRP (Responsabilidad Unica): su unica responsabilidad es modelar y exponer los datos propios
    del producto. No conoce nada sobre el registro de productos, la persistencia en archivos ni la
    interaccion por consola. PRINCIPIO OCP (Abierto/Cerrado): permite extender el catalogo a nuevos
    tipos de productos (como Bebida) mediante herencia, sin modificar la logica ya existente del servicio
    Restaurante ni de ArchivoServicio.

    MEJORA SEMANA 11: se incorpora el atributo "stock" para poder representar la cantidad disponible de
    cada producto y sostener la nueva operacion de venta (Usuario/Cliente + Producto -> Venta).
    """

    # Identifica el tipo de producto dentro del JSON para poder reconstruirlo
    # correctamente (Producto o Bebida) al cargar datos/productos.json.
    TIPO: str = "producto"

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int = 0,
    ) -> None:
        # Uso de anotaciones de tipos en el constructor y encapsulamiento mediante
        # propiedades (atributos protegidos con prefijo "_").
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        # MEJORA SEMANA 11: stock disponible del producto, validado en el setter.
        self.stock = stock

    # ---------------------------------------------------------------
    # Propiedades: acceso seguro y controlado a la informacion del producto.
    # ---------------------------------------------------------------
    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo del producto no puede estar vacio.")
        self._codigo = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacio.")
        self._nombre = nuevo_nombre.strip()

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, nueva_categoria: str) -> None:
        if not nueva_categoria or not nueva_categoria.strip():
            raise ValueError("La categoria del producto no puede estar vacia.")
        self._categoria = nueva_categoria.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio: float) -> None:
        try:
            precio_convertido = float(nuevo_precio)
        except (TypeError, ValueError):
            raise ValueError("El precio del producto debe ser un numero valido.")
        if precio_convertido <= 0:
            raise ValueError("El precio del producto debe ser mayor a cero.")
        self._precio = precio_convertido

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock: int) -> None:
        # MEJORA SEMANA 11: el stock siempre debe ser un entero valido y nunca negativo.
        try:
            stock_convertido = int(nuevo_stock)
        except (TypeError, ValueError):
            raise ValueError("El stock del producto debe ser un numero entero.")
        if stock_convertido < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        self._stock = stock_convertido

    # ---------------------------------------------------------------
    # Comportamiento
    # ---------------------------------------------------------------
    def vender(self, cantidad: int) -> bool:
        """
        MEJORA SEMANA 11: disminuye el stock cuando se realiza una venta valida.
        No conoce nada sobre Cliente ni sobre Venta: unicamente controla su propio
        estado interno (PRINCIPIO SRP), la relacion Usuario-Producto la administra
        el servicio Restaurante.
        """
        if cantidad <= 0 or self._stock < cantidad:
            return False
        self._stock -= cantidad
        return True

    def mostrar_informacion(self) -> str:
        """
        Define el comportamiento comun para presentar la informacion de cualquier producto. PRINCIPIO
        LSP (Sustitucion de Liskov): cualquier clase hija (por ejemplo Bebida) puede sustituir a Producto
        aqui sin alterar el comportamiento esperado por quien llama al metodo.
        """
        return (
            f"[Producto] Codigo: {self.codigo} | Nombre: {self.nombre} | "
            f"Categoria: {self.categoria} | Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock}"
        )

    def convertir_a_diccionario(self) -> dict:
        """
        Convierte el producto en una estructura compatible con JSON (dict) para que ArchivoServicio pueda
        guardarlo mediante json.dump(). Se incluye el campo "tipo" para que, al reconstruir la coleccion
        con json.load(), cada registro pueda volver a convertirse en el objeto correcto (Producto o Bebida).
        """
        return {
            "tipo": self.TIPO,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return self.mostrar_informacion()


