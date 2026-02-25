class Arbol:
    """
    Representa un arbol en los terrenos del castillo que provee recursos.
    """
    def __init__(self, tipo, frutos_iniciales, resistencia_frio):
        """
        Inicializa los atributos del arbol.

        Args:
            tipo (str): Especie del arbol (ej. Pino, Roble).
            frutos_iniciales (int): Cantidad de frutos disponibles al inicio.
            resistencia_frio (int): Capacidad de soportar el clima (0-100).
        """
        self.tipo = tipo
        self.frutos = frutos_iniciales
        self.resistencia_frio = resistencia_frio

    def regenerar(self):
        """
        Aumenta la cantidad de frutos si el arbol tiene suficiente resistencia.

        Returns:
            str: Mensaje sobre el estado de la regeneracion.
        """
        if self.resistencia_frio > 20:
            self.frutos += 5
            return f"El {self.tipo} esta muy debil por el frío para dar frutos. "
        
    def sufrir_frio(self, danio):
        """
        Reduce la resistencia del arbol debido al clima extremo.

        Args:
            danio (int): Cantidad de resistencia que pierde el arbol.
        """
        self.resistencia_frio -= danio
        if self.resistencia_frio < 0:
            self.resistencia_frio = 0