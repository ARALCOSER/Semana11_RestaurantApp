import os

os.system("cls")  # Limpiar la consola

import re
from pathlib import Path
from typing import Callable

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante
from servicios.archivo_servicio import ArchivoServicio

# TUPLA (tuple): utilizada para representar informacion que debe mantenerse estable durante la ejecucion,
# por ejemplo las opciones disponibles del menu principal. OPCIONES_MENU es una tupla de tuplas (numero,
# descripcion): son datos "quemados" definidos por el programador. El contenido del menu en si no se puede
# agregar, eliminar ni modificar mientras el programa esta en ejecucion, porque una tupla es inmutable.
#
# MEJORA SEMANA 11: se agregan las opciones 10 (Vender producto) y 11 (Consultar ventas de un cliente).
OPCIONES_MENU: tuple[tuple[str, str], ...] = (
    ("1", "Registrar producto"),
    ("2", "Registrar bebida"),
    ("3", "Buscar producto"),
    ("4", "Actualizar producto"),
    ("5", "Eliminar producto"),
    ("6", "Listar productos"),
    ("7", "Registrar cliente"),
    ("8", "Listar clientes"),
    ("9", "Mostrar categorias"),
    ("10", "Vender producto"),
    ("11", "Consultar ventas de un cliente"),
    ("0", "Salir"),
)

# TUPLA (tuple): igual que OPCIONES_MENU, guarda datos fijos (los numeros de opcion despues de los cuales se
# imprime una linea separadora) que tampoco deben modificarse en tiempo de ejecucion.
SEPARADORES_MENU: tuple[str, ...] = ("2", "6", "8", "9")


def mostrar_menu() -> None:
    """
    Imprime el menu recorriendo la TUPLA OPCIONES_MENU con un for, en lugar de
    repetir multiples print() sueltos por cada opcion.
    """
    print("\n==================================================")
    print("|        SISTEMA DE RESTAURANTE VACA & VACO      |")
    print("==================================================")
    print()
    for numero, descripcion in OPCIONES_MENU:
        print(f"{numero}. {descripcion}")
        if numero in SEPARADORES_MENU:
            print("-" * 50)
    print()


def validar_campo_vacio(valor: str, nombre_campo: str) -> bool:
    # Validaciones y manejo de excepciones para evitar que entradas incorrectas detengan el programa.
    if not valor:
        print(f"Error: El campo '{nombre_campo}' es obligatorio.")
        return False
    return True


def _solicitar_precio() -> float:
    # Validacion con manejo de excepcion (ValueError) para que un precio invalido no detenga el programa.
    while True:
        precio_raw = input("Precio: ").strip()
        if not validar_campo_vacio(precio_raw, "Precio"):
            continue
        try:
            precio = float(precio_raw)
            if precio <= 0:
                print("Error: El precio debe ser un valor mayor a cero.")
                continue
            return precio
        except ValueError:
            print("Error: El precio debe ser un numero valido.")


def _solicitar_entero(mensaje: str, permitir_cero: bool = True) -> int:
    # MEJORA SEMANA 11: validacion generica para leer enteros (stock, cantidad a vender),
    # evitando que un valor invalido detenga el programa.
    while True:
        texto = input(mensaje).strip()
        if not validar_campo_vacio(texto, "Cantidad"):
            continue
        try:
            valor = int(texto)
        except ValueError:
            print("Error: Debe ingresar un numero entero valido.")
            continue
        if valor < 0 or (valor == 0 and not permitir_cero):
            print("Error: El valor debe ser un entero mayor o igual a cero.")
            continue
        return valor


def guardar_productos(
    archivo_servicio: ArchivoServicio, restaurante: Restaurante
) -> None:
    """
    Solicita a ArchivoServicio que persista el estado actual de la coleccion de productos. Se llama despues
    de registrar, actualizar, eliminar o vender un producto correctamente. main.py no abre el archivo:
    solo coordina el momento en que debe guardarse.
    """
    guardado = archivo_servicio.guardar_productos(restaurante.obtener_productos())
    if not guardado:
        print("Advertencia: los cambios de productos no pudieron guardarse en el archivo.")


def guardar_clientes(
    archivo_servicio: ArchivoServicio, restaurante: Restaurante
) -> None:
    # MEJORA SEMANA 11: guardado automatico despues de registrar un cliente.
    guardado = archivo_servicio.guardar_clientes(restaurante.obtener_clientes())
    if not guardado:
        print("Advertencia: los cambios de clientes no pudieron guardarse en el archivo.")


def guardar_ventas(
    archivo_servicio: ArchivoServicio, restaurante: Restaurante
) -> None:
    # MEJORA SEMANA 11: guardado automatico despues de registrar una venta.
    guardado = archivo_servicio.guardar_ventas(restaurante.obtener_ventas())
    if not guardado:
        print("Advertencia: los cambios de ventas no pudieron guardarse en el archivo.")


def registrar_producto(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    print("\n--- REGISTRO DE PRODUCTO ---")
    while True:
        codigo = input("Codigo: ").strip()
        if validar_campo_vacio(codigo, "Codigo"):
            break
    while True:
        nombre = input("Nombre: ").strip()
        if validar_campo_vacio(nombre, "Nombre"):
            break
    while True:
        categoria = input(
            "Categoria (ej: sopa, plato fuerte, entrada, porciones, ensalada): "
        ).strip()
        if validar_campo_vacio(categoria, "Categoria"):
            break
    precio = _solicitar_precio()
    # MEJORA SEMANA 11: todo producto ahora se registra con un stock inicial disponible.
    stock = _solicitar_entero("Stock disponible: ")
    try:
        # Creacion del objeto Producto a partir de los datos ingresados y delegacion al servicio Restaurante
        # (main.py no administra la lista de productos directamente).
        producto = Producto(codigo, nombre, categoria, precio, stock)
    except ValueError as error:
        print(f"Error: {error}")
        return
    mensaje = restaurante.registrar_producto(producto)
    print(mensaje)
    if mensaje.startswith("El producto"):
        guardar_productos(archivo_servicio, restaurante)


def registrar_bebida(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    print("\n--- REGISTRO DE BEBIDA ---")
    while True:
        codigo = input("Codigo: ").strip()
        if validar_campo_vacio(codigo, "Codigo"):
            break
    while True:
        nombre = input("Nombre: ").strip()
        if validar_campo_vacio(nombre, "Nombre"):
            break
    while True:
        categoria = input(
            "Categoria (ej: gaseosa, jugo natural, bebida caliente): "
        ).strip()
        if validar_campo_vacio(categoria, "Categoria"):
            break
    precio = _solicitar_precio()
    while True:
        tamano = input("Tamano (ej: 100ml, 500ml, Grande): ").strip()
        if validar_campo_vacio(tamano, "Tamano"):
            break
    # MEJORA SEMANA 11: la bebida tambien maneja stock (heredado de Producto).
    stock = _solicitar_entero("Stock disponible: ")
    try:
        # Instanciacion correcta de la clase heredada Bebida con paso de parametros dinamicos ingresados por consola.
        bebida = Bebida(codigo, nombre, categoria, precio, tamano, stock)
    except ValueError as error:
        print(f"Error: {error}")
        return
    mensaje = restaurante.registrar_producto(bebida)
    print(mensaje)
    if mensaje.startswith("El producto"):
        guardar_productos(archivo_servicio, restaurante)


def buscar_producto(restaurante: Restaurante) -> None:
    print("\n--- BUSQUEDA DE PRODUCTO ---")
    while True:
        codigo = input("Codigo del producto a buscar: ").strip()
        if validar_campo_vacio(codigo, "Codigo"):
            break
    # Restriccion de arquitectura: main.py NO recorre la lista interna del servicio; delega la busqueda al
    # metodo buscar_producto_por_codigo() de Restaurante.
    producto = restaurante.buscar_producto_por_codigo(codigo)
    if producto is None:
        print(f"No se encontro ningun producto con el codigo {codigo}.")
        return
    print("Producto encontrado:")
    print(producto.mostrar_informacion())


def actualizar_producto(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    print("\n--- ACTUALIZACION DE PRODUCTO ---")
    while True:
        codigo = input("Codigo del producto a actualizar: ").strip()
        if validar_campo_vacio(codigo, "Codigo"):
            break
    if restaurante.buscar_producto_por_codigo(codigo) is None:
        print(f"Error: No existe un producto con el codigo {codigo}.")
        return

    print("Deje el campo vacio si no desea modificarlo.")
    nombre = input("Nuevo nombre: ").strip()
    categoria = input("Nueva categoria: ").strip()
    precio_raw = input("Nuevo precio: ").strip()
    stock_raw = input("Nuevo stock: ").strip()

    precio: float | None = None
    if precio_raw:
        try:
            precio = float(precio_raw)
            if precio <= 0:
                print("Error: El precio debe ser un valor mayor a cero.")
                return
        except ValueError:
            print("Error: El precio debe ser un numero valido.")
            return

    stock: int | None = None
    if stock_raw:
        try:
            stock = int(stock_raw)
            if stock < 0:
                print("Error: El stock no puede ser negativo.")
                return
        except ValueError:
            print("Error: El stock debe ser un numero entero valido.")
            return

    try:
        # Restriccion de arquitectura: la actualizacion real del producto ocurre dentro de
        # Restaurante.actualizar_producto, no accediendo directamente a la lista interna del servicio.
        mensaje = restaurante.actualizar_producto(
            codigo,
            nombre=nombre or None,
            categoria=categoria or None,
            precio=precio,
            stock=stock,
        )
    except ValueError as error:
        print(f"Error: {error}")
        return
    print(mensaje)
    if mensaje.startswith("El producto"):
        guardar_productos(archivo_servicio, restaurante)


def eliminar_producto(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    print("\n--- ELIMINACION DE PRODUCTO ---")
    while True:
        codigo = input("Codigo del producto a eliminar: ").strip()
        if validar_campo_vacio(codigo, "Codigo"):
            break
    mensaje = restaurante.eliminar_producto(codigo)
    print(mensaje)
    if mensaje.startswith("El producto"):
        guardar_productos(archivo_servicio, restaurante)


def registrar_cliente(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    print("\n--- REGISTRO DE CLIENTE ---")
    # Validacion de formato (10 digitos numericos) para evitar que una identificacion mal escrita detenga
    # el programa o ensucie la coleccion de clientes.
    while True:
        identificacion = input("Cedula de identidad: ").strip()
        if not validar_campo_vacio(identificacion, "Identificacion"):
            continue
        if not (identificacion.isdigit() and len(identificacion) == 10):
            print(
                "Error: La identificacion (cedula) debe contener exactamente "
                "10 digitos numericos."
            )
            continue
        break

    while True:
        nombre = input("Nombre: ").strip()
        if validar_campo_vacio(nombre, "Nombre"):
            break

    while True:
        correo = input("Correo (ej: pepe@hotmail.com): ").strip()
        if not validar_campo_vacio(correo, "Correo"):
            continue
        patron_correo = r"^[\w.-]+@[\w.-]+\.\w+$"
        if not re.match(patron_correo, correo):
            print("Error: El formato del correo electronico no es valido.")
            continue
        break

    try:
        # Creacion del objeto Cliente a partir de datos ingresados por consola y delegacion al
        # servicio Restaurante.
        cliente = Cliente(identificacion, nombre, correo)
    except ValueError as error:
        print(f"Error: {error}")
        return

    mensaje = restaurante.registrar_cliente(cliente)
    print(mensaje)
    # MEJORA SEMANA 11: ahora si se persiste el registro de clientes en usuarios.json.
    if mensaje.startswith("El cliente"):
        guardar_clientes(archivo_servicio, restaurante)


def vender_producto(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    """
    MEJORA SEMANA 11: opcion del menu para registrar la venta de un producto a un cliente.
    Aqui se demuestra la relacion Usuario (Cliente) + Producto -> Venta.
    """
    print("\n--- VENTA DE PRODUCTO ---")
    while True:
        identificacion_cliente = input("Identificacion del cliente: ").strip()
        if validar_campo_vacio(identificacion_cliente, "Identificacion"):
            break
    while True:
        codigo_producto = input("Codigo del producto: ").strip()
        if validar_campo_vacio(codigo_producto, "Codigo"):
            break

    # main.py solo consulta para dar mensajes claros al usuario; la regla final de negocio
    # siempre se valida (y se aplica) dentro de Restaurante.vender_producto().
    cliente = restaurante.buscar_cliente_por_identificacion(identificacion_cliente)
    if cliente is None:
        print("Error: No existe un cliente con esa identificacion.")
        return

    producto = restaurante.buscar_producto_por_codigo(codigo_producto)
    if producto is None:
        print("Error: No existe un producto con ese codigo.")
        return

    print(f"Producto: {producto.nombre} | Stock disponible: {producto.stock}")
    cantidad = _solicitar_entero("Cantidad a vender: ", permitir_cero=False)

    if producto.stock < cantidad:
        print("Error: No hay stock suficiente para esta venta.")
        return

    vendido = restaurante.vender_producto(codigo_producto, identificacion_cliente, cantidad)
    if vendido:
        print(
            f"Venta registrada correctamente para {cliente.nombre}. "
            f"Stock actual de {producto.nombre}: {producto.stock}"
        )
        # Una sola operacion modifica dos colecciones: se guardan la nueva venta y el
        # nuevo stock del producto.
        guardar_ventas(archivo_servicio, restaurante)
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("No fue posible registrar la venta.")


def consultar_ventas_cliente(restaurante: Restaurante) -> None:
    """
    MEJORA SEMANA 11: opcion del menu para consultar, mediante recorrido y filtrado de la
    coleccion de ventas, las ventas realizadas por un cliente especifico.
    """
    print("\n--- VENTAS DE UN CLIENTE ---")
    while True:
        identificacion_cliente = input("Identificacion del cliente: ").strip()
        if validar_campo_vacio(identificacion_cliente, "Identificacion"):
            break

    cliente = restaurante.buscar_cliente_por_identificacion(identificacion_cliente)
    if cliente is None:
        print("Error: No existe un cliente con esa identificacion.")
        return

    ventas_cliente = restaurante.consultar_ventas_cliente(identificacion_cliente)
    print(f"\nVentas registradas para {cliente.nombre}:")
    if not ventas_cliente:
        print("- Sin ventas registradas.")
        return

    for venta in ventas_cliente:
        producto = restaurante.buscar_producto_por_codigo(venta.producto_codigo)
        nombre_producto = producto.nombre if producto is not None else "Producto no encontrado"
        print(
            f"- Codigo: {venta.producto_codigo} | Producto: {nombre_producto} | "
            f"Cantidad: {venta.cantidad}"
        )


def mostrar_productos(restaurante: Restaurante) -> None:
    productos = restaurante.listar_productos()
    if not productos:
        print("\nNo existen productos o bebidas registrados.")
        return
    print("\n=== PRODUCTOS REGISTRADOS ===")
    for info in productos:
        print(info)
    print(f"\nTotal de productos registrados: {restaurante.contar_productos()}")


def mostrar_clientes(restaurante: Restaurante) -> None:
    clientes = restaurante.listar_clientes()
    if not clientes:
        print("\nNo existen clientes registrados.")
        return
    print("\n=== CLIENTES REGISTRADOS ===")
    for info in clientes:
        print(info)


def mostrar_categorias(restaurante: Restaurante) -> None:
    # El servicio retorna un CONJUNTO (set) de categorias unicas; aqui solo se
    # ordena con sorted() para presentarlo de forma legible, sin alterar su
    # naturaleza de valores sin duplicados.
    categorias = restaurante.obtener_categorias_unicas()
    if not categorias:
        print("\nNo existen categorias registradas todavia.")
        return
    print("\n=== CATEGORIAS UNICAS REGISTRADAS ===")
    for categoria in sorted(categorias):
        print(f"- {categoria}")


def main() -> None:
    # Se crea ArchivoServicio apuntando a la carpeta "datos" (ruta relativa a este archivo, para que
    # funcione sin importar desde donde se ejecute python) y se cargan productos, clientes y ventas
    # guardados ANTES de crear el menu. Los diccionarios leidos de cada JSON ya llegan convertidos en
    # objetos (Producto/Bebida, Cliente, Venta) gracias a ArchivoServicio.
    ruta_datos = Path(__file__).resolve().parent / "datos"
    archivo_servicio = ArchivoServicio(str(ruta_datos))

    productos_guardados = archivo_servicio.cargar_productos()
    clientes_guardados = archivo_servicio.cargar_clientes()
    ventas_guardadas = archivo_servicio.cargar_ventas()

    # Restriccion de arquitectura: "main.py no administra colecciones directamente." Toda la logica
    # interna de almacenamiento (listas y conjunto de categorias) esta delegada a la instancia de Restaurante.
    restaurante = Restaurante(productos_guardados, clientes_guardados, ventas_guardadas)

    if productos_guardados:
        print(f"Se cargaron {len(productos_guardados)} producto(s) desde datos/productos.json.")
    else:
        print("No se encontraron productos guardados. Se inicia con la lista vacia.")

    if clientes_guardados:
        print(f"Se cargaron {len(clientes_guardados)} cliente(s) desde datos/usuarios.json.")
    else:
        print("No se encontraron clientes guardados. Se inicia con la lista vacia.")

    if ventas_guardadas:
        print(f"Se cargaron {len(ventas_guardadas)} venta(s) desde datos/ventas.json.")
    else:
        print("No se encontraron ventas guardadas. Se inicia con la lista vacia.")

    # DICCIONARIO (dict): utilizado cuando existe una relacion clara de clave -> valor. Asocia las opciones
    # del menu con las funciones correspondientes. La clave es el numero de opcion escrito por consola
    # (coincide con el primer valor de cada tupla en OPCIONES_MENU); el valor es la funcion que ejecuta
    # esa accion. Esto reemplaza una larga cadena de if/elif por una busqueda directa en el diccionario.
    acciones: dict[str, Callable[[], None]] = {
        "1": lambda: registrar_producto(restaurante, archivo_servicio),
        "2": lambda: registrar_bebida(restaurante, archivo_servicio),
        "3": lambda: buscar_producto(restaurante),
        "4": lambda: actualizar_producto(restaurante, archivo_servicio),
        "5": lambda: eliminar_producto(restaurante, archivo_servicio),
        "6": lambda: mostrar_productos(restaurante),
        "7": lambda: registrar_cliente(restaurante, archivo_servicio),
        "8": lambda: mostrar_clientes(restaurante),
        "9": lambda: mostrar_categorias(restaurante),
        "10": lambda: vender_producto(restaurante, archivo_servicio),
        "11": lambda: consultar_ventas_cliente(restaurante),
    }

    # Implementa un menu interactivo ejecutado desde main.py, manteniendo el
    # programa en ejecucion hasta que se seleccione la opcion de salir.
    while True:
        mostrar_menu()
        opcion = input("Por favor seleccione una opcion -> : ").strip()
        if opcion == "0":
            print("\nHas finalizado correctamente.")
            print()
            break
        # USO DEL DICCIONARIO: dict.get() busca la funcion asociada a la opcion elegida; si la clave no
        # existe, se informa un error sin detener el programa.
        accion = acciones.get(opcion)
        if accion is None:
            print("\nError: Seleccione una opcion valida del menu.")
            continue
        accion()


if __name__ == "__main__":
    main()


