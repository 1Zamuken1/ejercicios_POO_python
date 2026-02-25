class Castillo:
    """Fortaleza que debe protegerse del invierno."""

    def __init__(self, nombre, integridad_inicial=100):
        self.nombre     = nombre
        self.integridad = integridad_inicial

    def refugiar_soldado(self, soldado):
        costo, recuperacion = 10, 25
        if self.integridad > costo:
            soldado.energia  += recuperacion
            self.integridad  -= costo
            return (f"{soldado.nombre} descansó al calor del fuego. "
                    f"Energía: {soldado.energia}. "
                    f"Integridad del castillo: {self.integridad}.")
        return "El castillo está muy deteriorado para ofrecer refugio seguro."

    def reparar(self, soldado):
        costo, puntos = 15, 20
        if soldado.energia >= costo:
            soldado.energia  -= costo
            self.integridad  += puntos
            if self.integridad > 100:
                self.integridad = 100
            return (f"{soldado.nombre} reparó los muros. "
                    f"Integridad del castillo: {self.integridad}.")
        return f"{soldado.nombre} no tiene energía suficiente para reparar."

    def recibir_danio_clima(self, danio):
        self.integridad -= danio
        if self.integridad < 0:
            self.integridad = 0
        return f"El castillo recibió {danio} puntos de daño por la tormenta de nieve."