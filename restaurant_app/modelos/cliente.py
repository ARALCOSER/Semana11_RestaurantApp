class Cliente:
    """
    Representa a un cliente registrado en el restaurante. PRINCIPIO SRP (Responsabilidad Unica): su unica responsabilidad es modelar y 
    exponer los datos propios del cliente (identificacion, nombre y correo). No conoce nada sobre el menu, el registro de productos ni 
    la interaccion por consola.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        # Uso de anotaciones de tipos de datos en el constructor y encapsulamiento mediante atributos protegidos. 
        # MEJORA SEMANA 11: se agregan validaciones basicas (ValueError) para que el cliente siempre quede en un estado valido,
        # tanto si se crea desde consola como si se reconstruye desde usuarios.json.

        if not identificacion or not identificacion.strip():
            raise ValueError("La identificacion del cliente no puede estar vacia.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacio.")
        if not correo or not correo.strip():
            raise ValueError("El correo del cliente no puede estar vacio.")

        self._identificacion = identificacion.strip()
        self._nombre = nombre.strip()
        self._correo = correo.strip()

    # Propiedades (@property) para exponer la informacion de forma controlada, sin permitir su modificacion directa desde fuera de la clase.

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    def mostrar_informacion(self) -> str:
        return (
            f"Cedula: {self.identificacion} | Nombre: {self.nombre} | "
            f"Correo: {self.correo}"
        )

    def convertir_a_diccionario(self) -> dict:
        """
        MEJORA SEMANA 11: permite que ArchivoServicio guarde al cliente en usuarios.json mediante json.dump(), completando la persistencia 
        que en la Semana 10 todavia no existia para esta entidad.
        """
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    def __str__(self) -> str:
        return self.mostrar_informacion()


