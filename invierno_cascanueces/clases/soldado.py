class Soldado:
    """El cascanueces encargado de la recolección y mantenimiento."""

    def __init__(self, nombre, energia_inicial=100):
        self.nombre  = nombre
        self.energia = energia_inicial

    def recolectar_frutos(self, arbol):
        costo = 10
        if self.energia <= costo:
            return f"{self.nombre} está demasiado cansado para ir al bosque."
        if arbol.frutos > 0:
            recolectado      = min(arbol.frutos, 10)
            arbol.frutos    -= recolectado
            self.energia    += recolectado * 3 - costo
            return (f"{self.nombre} recolectó {recolectado} frutos del {arbol.tipo}. "
                    f"Energía actual: {self.energia}.")
        self.energia -= costo
        return f"El {arbol.tipo} no tiene frutos. {self.nombre} gastó energía en vano."