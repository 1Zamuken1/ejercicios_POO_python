# El Invierno del Cascanueces

Un juego de simulación y gestión de recursos en POO (Programación Orientada a Objetos).

## Descripción

Juega como el **Cascanueces** y sobrevive **7 días de invierno** gestionando:
- **Castillo**: Estructura defensiva (integridad)
- **Soldado**: Tu personaje con energía
- **Árbol Mágico**: Proveedor de frutos (recursos)

Elige entre dos modos:
- 🖥️ **Terminal**: Solo texto, sin dependencias (recomendado para empezar)
- 🕹️ **Gráfico**: Con Pygame (pixel-art)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd invierno_cascanueces
```

### 2. Crear un entorno virtual
```bash
# En Windows:
python -m venv venv
venv\Scripts\activate

# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso

### Modo Terminal (sin Pygame)
```bash
python main.py --terminal
```

### Modo Gráfico (con Pygame)
```bash
python main.py --grafico
```

### Menú Interactivo
```bash
python main.py
```

## Estructura del Proyecto

```
invierno_cascanueces/
├── main.py                 # Punto de entrada
├── motor.py               # Lógica simple (versión alternativa)
├── requirements.txt       # Dependencias
├── clases/
│   ├── castillo.py       # Clase Castillo
│   ├── soldado.py        # Clase Soldado
│   └── arbol.py          # Clase Arbol
├── motor/
│   ├── __init__.py
│   └── estado.py         # NÚcleo del juego (EstadoJuego)
├── ui/
│   ├── terminal.py       # Interfaz por consola
│   ├── pygame_ui.py      # Interfaz gráfica
│   ├── hud.py            # Panel de interfaz (Pygame)
│   └── sprites.py        # Renderizado de sprites (Pygame)
└── recursos/
    └── arte_ascii.py     # Arte ASCII para consola
```

## Reglas del Juego

**Cada turno el jugador elige una acción:**
1. **Recolectar frutos**: Ganas energía, pero gastas energía de viaje
2. **Descansar**: Recuperas mucha energía, pero dañas el castillo
3. **Reparar muros**: Restauras el castillo, pero cuesta energía

**Después cada turno:**
- La tormenta ataca (daña castillo y árbol)
- El árbol se regenera si tiene resistencia

**Victoria**: Sobrevive los 7 días
**Derrota**: El castillo se destruye O el soldado se queda sin energía

## Notas de Desarrollo

Proyecto creado como ejemplo de **POO en Python** con:
- Clases con herencia y métodos
- Gestión de estado mutable
- Separación entre lógica de juego y interfaz (UI)
- Dos modos de juego sin duplicar código de lógica

## Autor

Ejercicio educativo - Programación Orientada a Objetos
