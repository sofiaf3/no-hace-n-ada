# tests/test_project.py
import math
import random
import sys
import os

# Añadir el directorio padre al path para importar project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project import Point, find_closest_pairs, brute_force_closest, generate_random_points

def test_no_points():
    """Test con lista vacía"""
    res = find_closest_pairs([])
    assert res.min_dist == float('inf')
    assert len(res.pairs) == 0

def test_one_point():
    """Test con un solo punto"""
    res = find_closest_pairs([Point(0, 0)])
    assert res.min_dist == float('inf')
    assert len(res.pairs) == 0

def test_two_points():
    """Test con dos puntos"""
    a = Point(0, 0)
    b = Point(3, 4)
    res = find_closest_pairs([a, b])
    assert abs(res.min_dist - 5.0) < 1e-9
    assert len(res.pairs) == 1
    assert (a, b) in res.pairs or (b, a) in res.pairs

def test_square_multiple_pairs():
    """Test con cuadrado - múltiples pares a misma distancia"""
    pts = [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)]
    res1 = find_closest_pairs(pts)
    res2 = brute_force_closest(pts)
    assert abs(res1.min_dist - res2.min_dist) < 1e-9
    assert abs(res1.min_dist - 1.0) < 1e-9
    assert len(res1.pairs) == 4

def test_duplicate_points():
    """Test con puntos duplicados"""
    pts = [Point(0, 0), Point(0, 0), Point(1, 1), Point(0, 0)]
    res = find_closest_pairs(pts)
    assert abs(res.min_dist - 0.0) < 1e-9
    assert len(res.pairs) >= 1

def test_three_points_same_distance():
    """Test triángulo equilátero"""
    height = math.sqrt(3) / 2
    pts = [Point(0, 0), Point(1, 0), Point(0.5, height)]
    res = find_closest_pairs(pts)
    assert abs(res.min_dist - 1.0) < 1e-9
    assert len(res.pairs) == 3

def test_random_compare_bruteforce():
    """Comparación con fuerza bruta"""
    pts = generate_random_points(15, 0, 100, 0, 100, seed=2025)
    res1 = find_closest_pairs(pts)
    res2 = brute_force_closest(pts)
    assert abs(res1.min_dist - res2.min_dist) < 1e-9

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