from __future__ import annotations
import math
import random
from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
import argparse
import tkinter as tk
from tkinter import ttk, messagebox
import time

@dataclass(frozen=True, order=True)
class Point:
    x: float
    y: float

def euclidean(a: Point, b: Point) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)

def find_close_pairs(points: List[Point], threshold: float) -> Set[Tuple[Point, Point]]:
    """
    Encuentra TODOS los pares de puntos que están a distancia <= threshold
    """
    close_pairs = set()
    
    # COMPARAR CADA PUNTO CON TODOS LOS DEMÁS
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = euclidean(points[i], points[j])
            if distance <= threshold:
                close_pairs.add((points[i], points[j]))
    
    return close_pairs

def generate_random_points(n: int, xmin: float, xmax: float, ymin: float, ymax: float, seed: Optional[int]=None) -> List[Point]:
    if seed is not None:
        random.seed(seed)
    return [Point(random.uniform(xmin, xmax), random.uniform(ymin, ymax)) for _ in range(n)]

class SimpleCollisionVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección de Colisiones - Visualización Simple")
        self.root.geometry("900x650")
        
        self.points: List[Point] = []
        self.close_pairs: Set[Tuple[Point, Point]] = set()
        self.canvas_width = 700
        self.canvas_height = 500
        self.margin = 50
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="🔍 Detección de Pares Cercanos", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Panel de control
        control_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
        # Controles
        ttk.Label(control_frame, text="Número de puntos:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.n_var = tk.StringVar(value="15")
        ttk.Entry(control_frame, textvariable=self.n_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(control_frame, text="Umbral de distancia:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.threshold_var = tk.StringVar(value="20.0")
        ttk.Entry(control_frame, textvariable=self.threshold_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(control_frame, text="Semilla:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.seed_var = tk.StringVar(value="42")
        ttk.Entry(control_frame, textvariable=self.seed_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Rango
        ttk.Label(control_frame, text="Rango (0 a 100):").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Botones
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Generar y Analizar", 
                  command=self.generate_and_analyze, width=15).grid(row=0, column=0, pady=5)
        ttk.Button(button_frame, text="Limpiar", 
                  command=self.clear_canvas, width=15).grid(row=1, column=0, pady=5)
        
        # Información
        info_frame = ttk.LabelFrame(control_frame, text="Resultados", padding="5")
        info_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.info_text = tk.Text(info_frame, height=10, width=25, font=("Courier", 8))
        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Canvas
        canvas_frame = ttk.LabelFrame(main_frame, text="Visualización", padding="10")
        canvas_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, 
                               bg="white", relief=tk.SUNKEN, bd=2)
        self.canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
    def scale_point(self, point: Point) -> tuple:
        """Convierte coordenadas reales a coordenadas del canvas"""
        xmin, xmax, ymin, ymax = 0, 100, 0, 100
        
        x = self.margin + (point.x - xmin) / (xmax - xmin) * (self.canvas_width - 2 * self.margin)
        y = self.canvas_height - self.margin - (point.y - ymin) / (ymax - ymin) * (self.canvas_height - 2 * self.margin)
        
        return x, y
    
    def generate_and_analyze(self):
        try:
            n = int(self.n_var.get())
            threshold = float(self.threshold_var.get())
            seed_text = self.seed_var.get().strip()
            
            if n < 2:
                messagebox.showerror("Error", "Debe haber al menos 2 puntos")
                return
            if threshold <= 0:
                messagebox.showerror("Error", "El umbral debe ser mayor que 0")
                return
            
            # Manejar semilla (puede estar vacía)
            seed = int(seed_text) if seed_text else None
            
            # Generar puntos
            self.points = generate_random_points(n, 0, 100, 0, 100, seed)
            
            # Encontrar pares cercanos
            start_time = time.time()
            self.close_pairs = find_close_pairs(self.points, threshold)
            end_time = time.time()
            
            # Mostrar resultados
            self.display_results(end_time - start_time, threshold)
            self.draw_all_points()
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor ingrese valores válidos")
    
    def display_results(self, execution_time: float, threshold: float):
        info = f"{'='*30}\n"
        info += f"Puntos: {len(self.points)}\n"
        info += f"Umbral: {threshold:.1f}\n"
        info += f"Tiempo: {execution_time*1000:.1f} ms\n"
        info += f"Pares cercanos: {len(self.close_pairs)}\n"
        info += f"{'='*30}\n\n"
        
        if self.close_pairs:
            # ORDENAR por distancia para mejor visualización
            sorted_pairs = sorted(self.close_pairs, key=lambda pair: euclidean(pair[0], pair[1]))
            
            info += "🔴 PARES CERCANOS DETECTADOS:\n"
            info += f"{'-'*25}\n"
            
            for i, (a, b) in enumerate(sorted_pairs, 1):
                dist = euclidean(a, b)
                info += f"Par {i}:\n"
                info += f"  A: ({a.x:5.1f}, {a.y:5.1f})\n"
                info += f"  B: ({b.x:5.1f}, {b.y:5.1f})\n"
                info += f"  📏 Distancia: {dist:.2f}\n"
                
                # Clasificar el riesgo (texto)
                if dist <= threshold * 0.5:
                    info += f"  🚨 ALTO RIESGO\n"
                elif dist <= threshold * 0.8:
                    info += f"  ⚠️  RIESGO MEDIO\n"
                else:
                    info += f"  🔶 RIESGO BAJO\n"
                    
                if i < len(sorted_pairs):
                    info += f"{'-'*20}\n"
        else:
            info += "✅ TODOS LOS PUNTOS ESTÁN SEGUROS\n"
            info += "No se detectaron pares cercanos\n"
            
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def draw_all_points(self):
        self.canvas.delete("all")
        
        # Dibujar fondo con cuadrícula
        self.draw_grid()
        
        # PRIMERO: Dibujar TODOS los puntos (azules)
        for point in self.points:
            x, y = self.scale_point(point)
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="blue", outline="darkblue", width=1)
            self.canvas.create_text(x, y-10, text=f"({point.x:.0f},{point.y:.0f})", 
                                  font=("Arial", 7), fill="blue")
        
        # Obtener umbral de manera segura
        try:
            threshold = float(self.threshold_var.get())
        except Exception:
            threshold = 0.0
        
        # LUEGO: Dibujar TODAS las líneas rojas para pares cercanos (según tu pedido)
        for a, b in self.close_pairs:
            x1, y1 = self.scale_point(a)
            x2, y2 = self.scale_point(b)
            dist = euclidean(a, b)
            
            # Para cumplir tu requerimiento: todas las parejas bajo el umbral conectadas con rojo.
            # Ajustamos el grosor según cuán cercano sea (más cercano -> línea más gruesa)
            if threshold > 0 and dist <= threshold * 0.5:
                color = "red"
                width = 3
            else:
                color = "red"
                width = 2
            
            # Línea conectando los puntos cercanos (todas en rojo)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            
            # Resaltar los puntos conectados (usar un contorno rojo claro)
            self.canvas.create_oval(x1-6, y1-6, x1+6, y1+6, fill="white", outline=color, width=2)
            self.canvas.create_oval(x2-6, y2-6, x2+6, y2+6, fill="white", outline=color, width=2)
            
            # Mostrar distancia en la línea (texto sin bg para evitar error)
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            self.canvas.create_text(mid_x, mid_y, text=f"{dist:.1f}", 
                                  fill="darkred", font=("Arial", 8, "bold"))
        
        # FINALMENTE: Leyenda
        self.draw_legend()
    
    def draw_grid(self):
        """Dibuja una cuadrícula para mejor referencia"""
        for i in range(0, 101, 20):
            # Líneas verticales
            x = self.margin + (i / 100) * (self.canvas_width - 2 * self.margin)
            self.canvas.create_line(x, self.margin, x, self.canvas_height - self.margin, 
                                  fill="lightgray", dash=(2, 2))
            self.canvas.create_text(x, self.canvas_height - 25, text=str(i), font=("Arial", 8))
            
            # Líneas horizontales  
            y = self.canvas_height - self.margin - (i / 100) * (self.canvas_height - 2 * self.margin)
            self.canvas.create_line(self.margin, y, self.canvas_width - self.margin, y, 
                                  fill="lightgray", dash=(2, 2))
            self.canvas.create_text(25, y, text=str(i), font=("Arial", 8))
    
    def draw_legend(self):
        """Dibuja la leyenda"""
        self.canvas.create_rectangle(10, 10, 25, 25, fill="blue", outline="black")
        self.canvas.create_text(35, 18, text="Aviones", anchor=tk.W, font=("Arial", 8))
        
        self.canvas.create_line(100, 18, 120, 18, fill="red", width=3)
        self.canvas.create_text(130, 18, text="Par bajo umbral", anchor=tk.W, font=("Arial", 8))
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.close_pairs = set()
        self.info_text.delete(1.0, tk.END)

def main():
    parser = argparse.ArgumentParser(description="Visualización simple de pares cercanos")
    parser.add_argument("--cli", action="store_true", help="Modo línea de comandos")
    parser.add_argument("--n", type=int, default=15, help="Número de puntos")
    parser.add_argument("--threshold", type=float, default=20.0, help="Umbral de distancia")
    parser.add_argument("--seed", type=int, default=42, help="Semilla aleatoria")
    
    args = parser.parse_args()
    
    if args.cli:
        points = generate_random_points(args.n, 0, 100, 0, 100, args.seed)
        close_pairs = find_close_pairs(points, args.threshold)
        
        print(f"Puntos generados: {len(points)}")
        print(f"Umbral: {args.threshold}")
        print(f"Pares cercanos encontrados: {len(close_pairs)}")
        print("-" * 50)
        
        # Ordenar por distancia
        sorted_pairs = sorted(close_pairs, key=lambda pair: euclidean(pair[0], pair[1]))
        
        for i, (a, b) in enumerate(sorted_pairs, 1):
            dist = euclidean(a, b)
            print(f"Par {i}:")
            print(f"  Punto A: ({a.x:.1f}, {a.y:.1f})")
            print(f"  Punto B: ({b.x:.1f}, {b.y:.1f})")
            print(f"  Distancia: {dist:.2f}")
            if i < len(sorted_pairs):
                print("-" * 30)
    else:
        root = tk.Tk()
        app = SimpleCollisionVisualizer(root)
        root.mainloop()

if __name__ == "__main__":
    main()
