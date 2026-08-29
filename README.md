# ✨ Restaurante App

🌟 **Estudiante:** Ramiro Alcoser A.

Proyecto académico en Python para practicar Programación Orientada a Objetos, colecciones, relaciones
entre objetos y persistencia JSON aplicada a `restaurante_app`.

Este repositorio corresponde a la **evolución de la Semana 11** del proyecto trabajado desde la Semana 10.
No es un sistema nuevo: se conservan `Producto`, `Bebida`, `Cliente` y todas las operaciones anteriores, y
se agregan las relaciones y operaciones propias del contexto de un restaurante que pide el sílabo de esta
semana (venta de productos, control de stock y persistencia completa).

## 🎯 Descripción del sistema

El sistema representa la administración de un restaurante: permite registrar, buscar, actualizar, eliminar
y listar productos y bebidas (con stock disponible); registrar y listar clientes; mostrar las categorías
únicas de los productos registrados; y, como mejora principal de esta semana, **vender productos a un
cliente**, controlando el stock disponible y dejando esa operación registrada en una colección de objetos
`Venta`. También permite **consultar las ventas realizadas por un cliente específico**. Toda la información
(productos, clientes y ventas) se guarda y se recupera automáticamente mediante archivos JSON, por lo que
persiste entre una ejecución y otra del programa.

## 🆕 Mejoras de la Semana 11

- Se agregó el atributo `stock` a `Producto` (heredado también por `Bebida`), con validación para que
  nunca quede en un valor negativo.
- Se creó el nuevo modelo `modelos/venta.py`, que representa la relación **Cliente (Usuario) + Producto →
  Venta**.
- Se implementó `Restaurante.vender_producto(codigo_producto, identificacion_cliente, cantidad)`, que
  valida que el cliente y el producto existan, que la cantidad sea mayor que cero y que exista stock
  suficiente antes de registrar la venta y descontar el stock.
- Se implementó `Restaurante.consultar_ventas_cliente(identificacion_cliente)`, que recorre y filtra la
  colección de ventas para mostrar únicamente las que pertenecen a un cliente.
- Se completó la persistencia de clientes (`usuarios.json`), que en la Semana 10 solo se manejaban en
  memoria.
- Se agregó la persistencia de ventas (`ventas.json`).
- `servicios/archivo_servicio.py` ahora centraliza la lectura y escritura de las tres colecciones
  (`productos.json`, `usuarios.json`, `ventas.json`) dentro de la misma carpeta `datos/`.
- `main.py` incorpora las opciones de menú **"Vender producto"** y **"Consultar ventas de un cliente"**, y
  ahora guarda automáticamente los clientes registrados (antes no se persistían).

## 🔥 Estructura del proyecto

```text
restaurante_app/
|
|-- datos/
|   |-- productos.json
|   |-- usuarios.json
|   `-- ventas.json
|
|-- modelos/
|   |-- __init__.py
|   |-- producto.py
|   |-- bebida.py
|   |-- cliente.py
|   `-- venta.py
|
|-- servicios/
|   |-- __init__.py
|   |-- archivo_servicio.py
|   `-- restaurante.py
|
|-- main.py
`-- README.md
```

## 🚀 Ejecución

Desde la carpeta `restaurante_app`, ejecutar:

```bash
python main.py
```

La aplicación carga automáticamente los archivos de `datos/` al iniciar (si todavía no existen, comienza
con listas vacías) y guarda los cambios después de cada operación importante.

## ✅ Responsabilidades

- **`modelos/producto.py`**: clase `Producto`, entidad base del sistema (código, nombre, categoría, precio
  y **stock**). Incluye `vender(cantidad)`, que disminuye el stock solo cuando la cantidad es válida.
- **`modelos/bebida.py`**: clase `Bebida`, que hereda de `Producto` y agrega el atributo `tamano`. Aplica
  herencia y polimorfismo (sobrescribe `mostrar_informacion()`), heredando también el manejo de stock.
- **`modelos/cliente.py`**: clase `Cliente`, que en este proyecto cumple el rol de **Usuario** que se
  relaciona con `Producto` mediante `Venta` (identificación, nombre y correo). Incluye
  `convertir_a_diccionario()` para su persistencia en `usuarios.json`.
- **`modelos/venta.py`** *(nuevo)*: clase `Venta`, que representa la relación entre un cliente
  (`usuario_id`), un producto (`producto_codigo`) y la `cantidad` vendida.
- **`servicios/restaurante.py`**: clase `Restaurante`, encargada de administrar las colecciones de
  productos, clientes y ventas, y de las operaciones de registro, búsqueda, actualización, eliminación,
  listado, **venta** y **consulta de ventas por cliente**. No interactúa con la consola (sin `input()` ni
  `print()`).
- **`servicios/archivo_servicio.py`**: clase `ArchivoServicio`, encargada de leer y guardar `productos.json`,
  `usuarios.json` y `ventas.json` mediante `json.load()` / `json.dump()` y `with open()`.
- **`main.py`**: contiene el menú de consola, la interacción por consola (`input()`) y la coordinación de
  las llamadas al servicio `Restaurante`; no administra directamente las colecciones internas.

## 📦 Funcionamiento del stock

Cada producto (incluidas las bebidas) maneja una cantidad disponible (`stock`), validada para que nunca sea
negativa. El stock se solicita al registrar un producto y puede modificarse al actualizarlo. Una venta solo
puede completarse si `stock >= cantidad` solicitada; de lo contrario, la operación se rechaza y ni el stock
ni la colección de ventas se modifican.

```text
Antes de vender
Producto: Hamburguesa
Stock: 10
Cantidad solicitada: 2

Después de vender
Producto: Hamburguesa
Stock: 8
Venta registrada correctamente
```

## 🔗 Relación Usuario (Cliente) – Producto mediante Venta

La operación `vender_producto()` del servicio `Restaurante` sigue este flujo:

```text
Cliente registrado
     ↓
Producto existente
     ↓
Validar cantidad solicitada (> 0)
     ↓
Validar stock disponible
     ↓
Crear Venta(usuario_id, producto_codigo, cantidad)
     ↓
Agregar Venta a la colección self._ventas
     ↓
Disminuir stock del producto (producto.vender(cantidad))
     ↓
Guardar ventas.json y productos.json
```

La consulta `consultar_ventas_cliente()` recorre `self._ventas` y filtra únicamente las que coinciden con la
identificación del cliente indicado, sin usar diccionarios sueltos: siempre se trabaja con objetos `Venta`.

## 💾 Persistencia de productos, usuarios y ventas

```text
Objetos (Producto/Bebida, Cliente, Venta)
        ↓
convertir_a_diccionario()
        ↓
lista de diccionarios
        ↓
json.dump()
        ↓
productos.json / usuarios.json / ventas.json
```

Al iniciar el programa ocurre el proceso inverso: `json.load()` reconstruye los diccionarios y estos se
convierten nuevamente en objetos del sistema.

Persistencia después de cada operación:

- Registrar, actualizar o eliminar un producto o bebida → se guarda `productos.json`.
- Registrar un cliente → se guarda `usuarios.json`.
- Realizar una venta → se guardan `ventas.json` **y** `productos.json` (una sola operación modifica dos
  colecciones a la vez: se agrega la venta y se descuenta el stock).

## ⚠️ Excepciones controladas

- **`FileNotFoundError`**: si `productos.json`, `usuarios.json` o `ventas.json` todavía no existen, la
  aplicación inicia con una colección vacía en lugar de detenerse.
- **`json.JSONDecodeError`**: si el contenido de alguno de los archivos no es un JSON válido, se informa por
  consola y se continúa con una lista vacía para esa colección.
- **`PermissionError`**: se controla tanto al leer como al guardar cada archivo, informando por consola sin
  detener la ejecución.
- **`KeyError`**: se controla al reconstruir productos, clientes y ventas desde JSON cuando falta una clave
  esperada en un registro; ese registro se omite y se informa.
- **`ValueError`**: se mantiene para las validaciones propias de `Producto` (precio, stock), `Cliente`
  (campos vacíos) y `Venta` (cantidad mayor a cero), tanto al crear objetos desde consola como al
  reconstruirlos desde JSON.

No se utiliza `except: pass` ni capturas genéricas para ocultar errores.

## 📚 Uso justificado de las estructuras de datos

El proyecto utiliza `list`, `tuple`, `dict` y `set` en lugares donde cada estructura cumple una
responsabilidad concreta dentro del sistema. No se reemplazan las clases `Producto`, `Bebida`, `Cliente` y
`Venta` por diccionarios; los diccionarios solo se usan como formato intermedio para la persistencia JSON.

### 📖 `list`: colecciones de productos, clientes y ventas

En `servicios/restaurante.py`, dentro de la clase `Restaurante`:

```python
self._productos: list[Producto] = []
self._clientes: list[Cliente] = []
self._ventas: list[Venta] = []
```

Las tres colecciones necesitan almacenar una cantidad variable de objetos que se agregan, buscan y recorren
constantemente (`append()` para registrar productos, clientes y ventas; `remove()` para eliminar productos;
`for` para buscar, listar y filtrar ventas por cliente).

### 📘 `tuple`: opciones fijas del menú

En `main.py`, `OPCIONES_MENU` sigue siendo una tupla de tuplas `(numero, descripcion)`: datos "quemados"
que no deben modificarse mientras el programa está en ejecución. Ahora incluye las nuevas opciones
**"Vender producto"** y **"Consultar ventas de un cliente"**.

### 📕 `dict`: relación entre claves y valores

En `main()`, el diccionario `acciones` sigue relacionando cada número de opción con la función que debe
ejecutarse (incluidas las nuevas funciones `vender_producto` y `consultar_ventas_cliente`), evitando una
larga cadena de `if`/`elif`.

### ✍️ `set`: categorías sin duplicados

`Restaurante.obtener_categorias_unicas()` sigue usando un `set` para mostrar cada categoría de producto una
única vez, sin importar cuántos productos la compartan.

## 📊 Menú principal

1. Registrar producto
2. Registrar bebida
3. Buscar producto
4. Actualizar producto
5. Eliminar producto
6. Listar productos
7. Registrar cliente
8. Listar clientes
9. Mostrar categorías
10. Vender producto
11. Consultar ventas de un cliente
0. Salir

## 🧪 Pruebas realizadas

- Se registró un cliente y un producto con stock inicial, y se verificó que ambos quedaran guardados en
  `usuarios.json` y `productos.json` respectivamente.
- Se realizó una venta válida (cantidad menor o igual al stock disponible): el stock del producto disminuyó
  correctamente, la venta quedó registrada en `ventas.json` y también se reflejó al consultar las ventas de
  ese cliente.
- Se intentó una venta con una cantidad mayor al stock disponible: la operación fue rechazada y ni
  `productos.json` ni `ventas.json` se modificaron.
- Se cerró el programa y se volvió a ejecutar `main.py`: productos, clientes y ventas se recuperaron
  correctamente desde sus archivos JSON, confirmando que la persistencia es real y no solo en memoria.
- Se verificó que `main.py` nunca recorre ni modifica directamente `self._productos`, `self._clientes` ni
  `self._ventas`: toda la lógica de negocio permanece dentro de `Restaurante`.

