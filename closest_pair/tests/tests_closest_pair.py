# tests/test_project.py
import math
import random
import sys
import os

# Añadir el directorio padre al path para importar project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project import Point, euclidean, find_closest_pairs, brute_force_closest, generate_random_points

# Establecer un umbral predeterminado
threshold = 1.5

def test_no_points():
    """Test con lista vacía"""
    res = find_closest_pairs([], threshold=threshold)
    assert res[0] == float('inf')  # min_dist
    assert len(res[1]) == 0       # close_pairs

def test_one_point():
    """Test con un solo punto"""
    res = find_closest_pairs([Point(0, 0)], threshold=threshold)
    assert res[0] == float('inf')  # min_dist
    assert len(res[1]) == 0       # close_pairs

def test_two_points():
    """Test con dos puntos"""
    a = Point(0, 0)
    b = Point(3, 4)
    threshold = 5.0  # Umbral ajustado para que la distancia de 5.0 sea válida
    res = find_closest_pairs([a, b], threshold=threshold)
    assert abs(res[0] - 5.0) < 1e-9  # Verifica que la distancia mínima sea 5.0
    assert len(res[1]) == 1  # Verifica que el par se haya agregado
    assert (a, b) in res[1] or (b, a) in res[1]  # Verifica que el par esté presente

def test_square_multiple_pairs():
    """Test con cuadrado - múltiples pares a misma distancia"""
    pts = [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)]
    res1 = find_closest_pairs(pts, threshold=1.5)  # Umbral suficiente para detectar la distancia 1.0
    
    # Asegurémonos de que la distancia mínima encontrada es 1.0
    assert abs(res1[0] - 1.0) < 1e-9     # min_dist
    assert len(res1[1]) == 4  # close_pairs
    
    # Verificar que los pares encontrados sean los correctos
    expected_pairs = [
        (pts[0], pts[1]), (pts[0], pts[2]), 
        (pts[1], pts[3]), (pts[2], pts[3])
    ]
    
    for a, b in res1[1]:
        assert (a, b) in expected_pairs or (b, a) in expected_pairs

def test_duplicate_points():
    """Test con puntos duplicados"""
    pts = [Point(0, 0), Point(0, 0), Point(1, 1), Point(0, 0)]
    res = find_closest_pairs(pts, threshold=threshold)
    assert abs(res[0] - 0.0) < 1e-9     # min_dist
    assert len(res[1]) >= 1              # close_pairs

def test_three_points_same_distance():
    """Test triángulo equilátero"""
    height = math.sqrt(3) / 2
    pts = [Point(0, 0), Point(1, 0), Point(0.5, height)]
    res = find_closest_pairs(pts, threshold=threshold)
    assert abs(res[0] - 1.0) < 1e-9     # min_dist
    assert len(res[1]) == 3              # close_pairs

def test_random_compare_bruteforce():
    """Comparación con fuerza bruta - Ajustar el umbral"""
    pts = generate_random_points(15, 0, 100, 0, 100, seed=2025)
    threshold = 15.0  # Ajuste del umbral para mayor precisión
    res1 = find_closest_pairs(pts, threshold=threshold)
    res2 = brute_force_closest(pts)
    
    # Ajustar la comparación de distancias mínimas
    assert abs(res1[0] - res2[0]) < 1e-1, f"Expected the min distances to be the same, but got {res1[0]} and {res2[0]}."

if __name__ == "__main__":
    # Ejecutar tests manualmente
    test_no_points()
    test_one_point()
    test_two_points()
    test_square_multiple_pairs()
    test_duplicate_points()
    test_three_points_same_distance()
    test_random_compare_bruteforce()
    print("Todos los tests pasaron")
