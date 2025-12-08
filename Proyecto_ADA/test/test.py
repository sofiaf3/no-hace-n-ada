import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Project import SistemaControlAereo, Aeronave, generar_aeronaves, distancia, encontrar_pares_cercanos, encontrar_par_mas_cercano

# Test para la generación de aeronaves
def test_generar_aeronaves():
    n = 5
    aeronaves = generar_aeronaves(n)
    assert len(aeronaves) == n, f"Se esperaban {n} aeronaves, pero se generaron {len(aeronaves)}"
    assert all(0 <= a.x <= 100 and 0 <= a.y <= 100 for a in aeronaves), "Las aeronaves tienen coordenadas fuera del rango esperado"

# Test para la función de distancia
def test_distancia():
    a1 = Aeronave(0, 0)
    a2 = Aeronave(3, 4)
    d = distancia(a1, a2)
    assert d == 5.0, f"Se esperaba una distancia de 5.0, pero se obtuvo {d}"

# Test para la función de encontrar pares cercanos
def test_encontrar_pares_cercanos():
    aeronaves = [Aeronave(0, 0), Aeronave(3, 4), Aeronave(6, 8)]
    umbral = 5.0
    pares_cercanos = encontrar_pares_cercanos(aeronaves, umbral)
    assert len(pares_cercanos) == 1, f"Se esperaban 1 par cercano, pero se encontraron {len(pares_cercanos)}"
    assert (pares_cercanos[0][0], pares_cercanos[0][1]) == (aeronaves[0], aeronaves[1]), "El par cercano detectado es incorrecto"

# Test para la función de encontrar el par más cercano
def test_encontrar_par_mas_cercano():
    aeronaves = [Aeronave(0, 0), Aeronave(3, 4), Aeronave(6, 8)]
    umbral = 5.0
    pares_cercanos = encontrar_pares_cercanos(aeronaves, umbral)
    par_mas_cercano = encontrar_par_mas_cercano(pares_cercanos)
    assert par_mas_cercano == (aeronaves[0], aeronaves[1]), f"Se esperaba el par más cercano (0, 0) y (3, 4), pero se obtuvo {par_mas_cercano}"

# Test para la funcionalidad de limpiar la simulación
def test_limpiar():
    ventana = None  # Se puede colocar un mock si es necesario
    app = SistemaControlAereo(ventana)
    
    # Generar aeronaves
    app.var_n.set("5")
    app.generar_aeronaves()
    assert len(app.aeronaves) == 5, "Se esperaban 5 aeronaves antes de limpiar"
    
    # Limpiar la simulación
    app.limpiar()
    
    # Verificar que la lista de aeronaves esté vacía
    assert len(app.aeronaves) == 0, "Las aeronaves no fueron eliminadas correctamente al limpiar"

# Test para la funcionalidad de análisis de los pares cercanos
def test_analizar():
    ventana = None  # Se puede colocar un mock si es necesario
    app = SistemaControlAereo(ventana)
    
    # Generar aeronaves
    app.var_n.set("10")
    app.generar_aeronaves()
    
    # Establecer umbral y ejecutar análisis
    app.var_umbral.set("15.0")
    app.analizar()
    
    # Verificar que los resultados del análisis fueron actualizados
    assert app.texto_resultados.get(1.0, 'end-1c') != "", "El análisis no generó resultados"
