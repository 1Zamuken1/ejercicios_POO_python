# Objeto: Tarjeta de crédito
# Atributo: Código de seguridad, numero cuenta, cvv, color, peso, material, cupo, chip, relieve, nombre del banco, tipo, franquisia, días de mora, intereses

# Crear clase
class TarjetaCredito:
    """
    Representa una tarjeta de credito con sus operaciones basicas.
    """

    # constructor -> Método que me permite inicializar los atributos de un objeto
    def __init__(self, numero, cupo, fecha_vencimiento, tipo, cvv, franquicia, pin):
        """
        Inicializa los atributos de la tarjeta.

        Args:
            numero (str): Numero identificador de la tarjeta.
            cupo (float): Saldo disponible para compras.
            fecha_vencimiento (str): Fecha de expiracion.
            tipo (str): Categoria de la tarjeta.
            cvv (int): Codigo de seguridad.
            franquicia (str): Empresa emisora (Visa/Mastercard).
            pin (int): Clave numerica de acceso.
        """
        # Atributos -> self
        self.numero = numero
        self.cupo = float(cupo)
        self.fecha_vencimiento = fecha_vencimiento
        self.tipo = tipo
        self.cvv = cvv
        self.franquicia = franquicia
        self.pin = pin

    # Métodos
    def validar_pin(self, pin_ingresado):
        """
        Compara el pin ingresado con el pin de la tarjeta.

        Args:
            pin_ingresado (int): El pin a verificar.
        Returns:
            bool: True si coinciden, False de lo contrario.
        """
        return self.pin == pin_ingresado

    def comprar(self, monto, pin_ingresado):
        """
        Realiza un descuento en el cupo si el pin es correcto y hay fondos.

        Args:
            monto (float): Valor de la transaccion.
            pin_ingresado (int): Clave para autorizar.
        Returns:
            str: Mensaje con el resultado de la operacion.
        """
        if not self.validar_pin(pin_ingresado):
            return "Error: PIN incorrecto."
        
        if monto > self.cupo:
            return f"Error: Cupo insuficiente. Cupo actual: {self.cupo}"
        
        self.cupo -= monto
        return f"Compra exitosa. Nuevo cupo: {self.cupo}"

# --- Funciones de Validacion de Entrada ---

def solicitar_dato(mensaje, tipo):
    """
    Solicita un dato y asegura que sea del tipo correcto mediante un bucle.

    Args:
        mensaje (str): Texto que se muestra al usuario.
        tipo (type): El tipo de dato esperado (int o float).
    Returns:
        int/float: El valor validado ingresado por el usuario.
    """
    while True:
        try:
            valor = tipo(input(mensaje))
            return valor
        except ValueError:
            print(f"Error: Se esperaba un valor de tipo {tipo.__name__}. Intente de nuevo.")

# --- Lógica de Ejecución ---

# Instanciar
cuentas = {
    "1234": TarjetaCredito("1234", 1000.0, "12/26", "Oro", 524, "Visa", 1111),
    "5678": TarjetaCredito("5678", 500.0, "10/25", "Clasica", 111, "Mastercard", 2222)
}

def app():
    """
    Controla el flujo principal del programa.
    """
    while True:
        print("\n--- SISTEMA BANCARIO ---")
        num = input("Ingrese numero de tarjeta o 'salir': ")
        
        if num.lower() == 'salir':
            break
            
        if num in cuentas:
            t = cuentas[num]
            pin_u = solicitar_dato("Ingrese su PIN: ", int)
            monto = solicitar_dato("Monto a comprar: ", float)
            
            print(t.comprar(monto, pin_u))
        else:
            print("Error: Tarjeta no encontrada.")

if __name__ == "__main__":
    app()