class Castillo:
    """
    Representa la base principal que debe protegerse del invierno.
    """

    def __init__(self, nombre, integridad_inicial=100):
        """
        Inicializa los atributos del castillo.

        Args:
            nombre (str): Nombre de la fortaleza.
            integridad_inicial (int): Nivel de salud o estado de los muros.
        """
        self.nombre = nombre
        self.integridad = integridad_inicial

    def refugiar_soldado(self, soldado):
        """
        Restaura energia al soldado a costa de consumir recursos (integridad) del castillo.

        Args:
            soldado (Soldado): Instancia del soldado que descansa.

        Returns:
            str: Resultado de la accion de descanso.
        """
        costo_calefaccion = 10
        recuperacion = 25

        if self.integridad > costo_calefaccion:
            soldado.energia += recuperacion
            self.integridad -= costo_calefaccion
            return f"{soldado.nombre} descanso al calor del fuego. Energia: {soldado.energia}. Integridad del castillo bajo a {self.integridad}."
        
        return "El castillo esta muy deteriorado para ofrecer un refugio seguro."

    def reparar(self, soldado):
        """
        Permite que el soldado gaste energia para subir la integridad del castillo.

        Args:
            soldado (Soldado): Instancia del soldado que repara.

        Returns:
            str: Resultado de la accion de reparacion.
        """
        costo_energia = 15
        puntos_reparacion = 20

        if soldado.energia >= costo_energia:
            soldado.energia -= costo_energia
            self.integridad += puntos_reparacion
            
            # Limitar la integridad maxima a 100
            if self.integridad > 100:
                self.integridad = 100
                
            return f"{soldado.nombre} reparo los muros. Integridad del castillo: {self.integridad}."
        
        return f"{soldado.nombre} no tiene energia suficiente para trabajar en las reparaciones."

    def recibir_danio_clima(self, danio):
        """
        Reduce la integridad del castillo debido al clima.

        Args:
            danio (int): Cantidad de danio recibido.

        Returns:
            str: Mensaje con el danio sufrido.
        """
        self.integridad -= danio
        if self.integridad < 0:
            self.integridad = 0
        return f"El castillo recibio {danio} puntos de danio por la tormenta de nieve."