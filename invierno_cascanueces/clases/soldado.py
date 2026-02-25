class Soldado:
    """
    Representa al cascanueces encargado de la recoleccion y mantenimiento.
    """

    def __init__(self, nombre, energia_inicial = 100):
        """
        Inicializa los atributos del cascanueces.

        Args:
            nombre (str): Nombre o identificador del soldado.
            energia_inicial (int): Nivel de energia al comenzar el juego.
        """
        self.nombre = nombre
        self.energia = energia_inicial

    def recolectar_frutos(self, arbol):
        """
        Interactua con un objeto Arbol para obtener frutos y recuperar energia.
        Consume energia al realizar la accion.

        Args:
            arbol (Arbol): Instancia de la clase Arbol.

        Returns:
            str: Mensaje indicando el resultado de la recoleccion.
        """
        costo_accion = 10
        if self.energia <= costo_accion:
            return f"{self.nombre} está demasiado cansado para ir al bosque"
        
        if arbol.frutos > 0:
            # Recolecta un máximo de 10 por turno
            recolectado = min(arbol.frutos, 10)
            arbol.frutos -= recolectado

            # Cada fruto da 3 de energía, pero la acción cuesta 10
            ganancia_energia = recolectado * 3
            self.energia = self.energia + ganancia_energia - costo_accion
            return f"{self.nombre} recolectó {recolectado} frutos del {arbol.tipo}. Energía actual: {self.energia}."
        else:
            self.energia -= costo_accion
            return f"El {arbol.tipo} no tiene frutos. {self.nombre} gasto de enería en vano."