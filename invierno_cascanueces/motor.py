import random
from clases.castillo import Castillo
from clases.soldado import Soldado
from clases.arbol import Arbol
from recursos.arte_ascii import CASTILLO_ASCII

def solicitar_opcion(mensaje, opciones_validas):
    """
    Solicita una entrada al usuario y valida que sea un numero entero
    dentro de una lista de opciones permitidas usando bucle y try-except.

    Args:
        mensaje (str): El texto que se mostrara en la consola.
        opciones_validas (list): Lista de enteros permitidos.

    Returns:
        int: La opcion validada ingresada por el usuario.
    """
    while True:
        try:
            opcion = int(input(mensaje))
            if opcion in opciones_validas:
                return opcion
            else:
                print(f"Error: Opcion no valida. Elija una de estas: {opciones_validas}.")
        except ValueError:
            print("Error: Entrada no valida. Por favor ingresa un numero entero.")

def iniciar_partida():
    """
    Controla el bucle principal del juego y la interaccion entre objetos.
    """
    # 1. Instanciar los objetos
    mi_castillo = Castillo("Fortaleza del Norte")
    mi_soldado = Soldado("Cascanueces")
    mi_arbol = Arbol("Pino Magico", frutos_iniciales=15, resistencia_frio=100)

    dias_transcurridos = 1
    dias_para_sobrevivir = 7 # Condicion de victoria

    # Bucle principal del juego
    while dias_transcurridos <= dias_para_sobrevivir and mi_castillo.integridad > 0 and mi_soldado.energia > 0:
        print("\n" + "="*40)
        print(f"--- DIA {dias_transcurridos} DE INVIERNO ---")
        print(CASTILLO_ASCII)
        
        # Mostrar el estado de todos los objetos
        print(f"[CASTILLO] Integridad: {mi_castillo.integridad}%")
        print(f"[SOLDADO]  Energia: {mi_soldado.energia}")
        print(f"[ARBOL]    Frutos: {mi_arbol.frutos} | Resistencia: {mi_arbol.resistencia_frio}")
        
        # Menú de consola
        print("\n¿Que orden le daras al soldado?")
        print("1. Ir al bosque a recolectar frutos (Restaura energia, cuesta energia de viaje)")
        print("2. Descansar en el castillo (Restaura mucha energia, daña el castillo)")
        print("3. Reparar el castillo (Cuesta energia, restaura el castillo)")
        
        opcion = solicitar_opcion("Elige una accion (1-3): ", [1, 2, 3])
        print("\n--- RESULTADO DE LA ACCION ---")
        
        # Interacciones POO
        if opcion == 1:
            print(mi_soldado.recolectar_frutos(mi_arbol))
        elif opcion == 2:
            print(mi_castillo.refugiar_soldado(mi_soldado))
        elif opcion == 3:
            print(mi_castillo.reparar(mi_soldado))

        # Turno del entorno (El clima ataca a los objetos pasivos)
        print("\n--- REPORTE CLIMATICO ---")
        danio_tormenta = random.randint(5, 15) # Daño aleatorio entre 5 y 15
        
        print(mi_castillo.recibir_danio_clima(danio_tormenta))
        mi_arbol.sufrir_frio(danio_tormenta // 2) # El arbol recibe la mitad del daño
        print(mi_arbol.regenerar())

        dias_transcurridos += 1

    # Condiciones de fin de juego
    print("\n" + "="*40)
    if mi_castillo.integridad <= 0:
        print("Derrota: Los muros del castillo han colapsado.")
    elif mi_soldado.energia <= 0:
        print("Derrota: El cascanueces se ha congelado al quedarse sin energia.")
    else:
        print("¡VICTORIA! Has sobrevivido a la tormenta de invierno.")