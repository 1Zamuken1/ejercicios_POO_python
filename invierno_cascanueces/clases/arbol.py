class Arbol:
    """Árbol que provee recursos al castillo."""

    def __init__(self, tipo, frutos_iniciales, resistencia_frio):
        self.tipo            = tipo
        self.frutos          = frutos_iniciales
        self.resistencia_frio = resistencia_frio

    def regenerar(self):
        if self.resistencia_frio > 20:
            self.frutos += 5
            return f"El {self.tipo} regeneró 5 frutos."
        return f"El {self.tipo} está muy débil para dar frutos."

    def sufrir_frio(self, danio):
        self.resistencia_frio = max(0, self.resistencia_frio - danio)