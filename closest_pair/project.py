"""
Sistema de Detección de Colisiones Aéreas
Implementación PURA del algoritmo Divide y Vencer
Proyecto Final - Análisis y Diseño de Algoritmos
"""

from __future__ import annotations
import math
import random
from typing import List, Tuple, Optional
import tkinter as tk
from tkinter import ttk, messagebox


# CLASES BÁSICAS

class Aeronave:
    """Representa una aeronave con coordenadas (x, y) en el espacio aéreo"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x:.1f}, {self.y:.1f})"

def distancia(a1: Aeronave, a2: Aeronave) -> float:
    """Calcula la distancia euclidiana entre dos aeronaves"""
    return math.hypot(a1.x - a2.x, a1.y - a2.y)

# ALGORITMO DIVIDE Y VENCER


def encontrar_pares_cercanos(aeronaves, umbral):
    # PRE: Asignar ID único a cada aeronave
    for i, a in enumerate(aeronaves):
        a.id = i
    
    def dividir_y_vencer(puntos_x, puntos_y):
        n = len(puntos_x)
        
        if n <= 3:
            pares = []
            for i in range(n):
                for j in range(i + 1, n):
                    if distancia(puntos_x[i], puntos_x[j]) <= umbral:
                        pares.append((puntos_x[i], puntos_x[j]))
            return pares
        
        mitad = n // 2
        punto_medio = puntos_x[mitad]
        
        # CORRECCIÓN: Distribuir puntos correctamente
        puntos_izq_x = puntos_x[:mitad]
        puntos_der_x = puntos_x[mitad:]
        
        puntos_izq_y = []
        puntos_der_y = []
        for p in puntos_y:
            if p.x < punto_medio.x:
                puntos_izq_y.append(p)
            elif p.x > punto_medio.x:
                puntos_der_y.append(p)
            else:
                # Misma x: usar ID para distribuir
                if p.id < punto_medio.id:
                    puntos_izq_y.append(p)
                else:
                    puntos_der_y.append(p)
        
        # Recursión
        pares_izq = dividir_y_vencer(puntos_izq_x, puntos_izq_y)
        pares_der = dividir_y_vencer(puntos_der_x, puntos_der_y)
        pares_totales = pares_izq + pares_der
        
        # MEJORA: Limitar comparaciones en banda
        banda = [p for p in puntos_y if abs(p.x - punto_medio.x) < umbral]
        
        # Solo comparar puntos cercanos en Y
        for i in range(len(banda)):
            # Solo comparar con los siguientes 7 puntos (optimización)
            for j in range(i + 1, min(i + 8, len(banda))):
                if banda[j].y - banda[i].y > umbral:
                    break
                
                if distancia(banda[i], banda[j]) <= umbral:
                    pares_totales.append((banda[i], banda[j]))
        
        return pares_totales
    
    # Ordenar con desempate
    puntos_x = sorted(aeronaves, key=lambda a: (a.x, a.y, a.id))
    puntos_y = sorted(aeronaves, key=lambda a: (a.y, a.x, a.id))
    
    return dividir_y_vencer(puntos_x, puntos_y)

def encontrar_par_mas_cercano(pares_cercanos: List[Tuple[Aeronave, Aeronave]]) -> Optional[Tuple[Aeronave, Aeronave]]:
    """Encuentra el par con menor distancia entre todos los pares cercanos"""
    if not pares_cercanos:
        return None
    
    # Ordenar por distancia ascendente
    pares_ordenados = sorted(pares_cercanos, key=lambda p: distancia(p[0], p[1]))
    return pares_ordenados[0]  # El primero es el más cercano

# GENERACIÓN DE DATOS


def generar_aeronaves(n: int) -> List[Aeronave]:
    """Genera n aeronaves en posiciones aleatorias (0-100 en ambos ejes)"""
    return [Aeronave(random.uniform(0, 100), random.uniform(0, 100)) 
            for _ in range(n)]

# INTERFAZ GRÁFICA


class SistemaControlAereo:
    """Interfaz gráfica del sistema de control aéreo"""
    
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("✈️ Sistema de Control Aéreo - Divide y Vencer")
        self.ventana.geometry("950x700")
        
        # Datos
        self.aeronaves = []
        self.pares_cercanos = []
        self.par_mas_cercano = None
        
        # Configuración visual
        self.ancho_canvas = 750
        self.alto_canvas = 550
        self.margen = 60
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea todos los componentes de la interfaz"""
        
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Título
        titulo = ttk.Label(
            main_frame,
            text="ALGORITMO DIVIDE Y VENCER - DETECCIÓN DE COLISIONES",
            font=("Arial", 16, "bold"),
            foreground="darkblue"
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # PANEL DE CONTROL 
        control_frame = ttk.LabelFrame(main_frame, text="CONTROLES", padding="15")
        control_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 15))
        
        # Número de aeronaves
        ttk.Label(control_frame, text="Número de aeronaves:", 
                 font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=8)
        
        self.var_n = tk.StringVar(value="30")
        ttk.Entry(control_frame, textvariable=self.var_n, width=12).grid(row=0, column=1, pady=8)
        
        # Separador
        ttk.Separator(control_frame, orient="horizontal").grid(row=1, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        
        # Umbral
        ttk.Label(control_frame, text="Umbral de distancia:", 
                 font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=8)
        
        self.var_umbral = tk.StringVar(value="20.0")
        ttk.Entry(control_frame, textvariable=self.var_umbral, width=12).grid(row=2, column=1, pady=8)
        
        ttk.Label(control_frame, text="Distancias ≤ este valor\nse consideran riesgosas",
                 font=("Arial", 8), foreground="gray").grid(row=3, column=0, columnspan=2, pady=5)
        
        # Separador
        ttk.Separator(control_frame, orient="horizontal").grid(row=4, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        # Botones
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Generar", 
                  command=self.generar_aeronaves, width=15).grid(row=0, column=0, pady=5)
        
        ttk.Button(btn_frame, text=" Analizar", 
                  command=self.analizar, width=15).grid(row=1, column=0, pady=5)
        
        ttk.Button(btn_frame, text=" Limpiar", 
                  command=self.limpiar, width=15).grid(row=2, column=0, pady=5)
        
        # PANEL DE RESULTADOS 
        resultados_frame = ttk.LabelFrame(control_frame, text="RESULTADOS", padding="10")
        resultados_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        
        # Texto de resultados
        self.texto_resultados = tk.Text(
            resultados_frame,
            height=18,
            width=35,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#f8f9fa"
        )
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.texto_resultados.yview)
        self.texto_resultados.configure(yscrollcommand=scrollbar.set)
        
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar expansión
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        control_frame.rowconfigure(6, weight=1)
        
        # CANVAS DE VISUALIZACIÓN 
        canvas_frame = ttk.LabelFrame(main_frame, text="VISUALIZACIÓN", padding="10")
        canvas_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Configurar expansión
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Canvas
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.ancho_canvas,
            height=self.alto_canvas,
            bg="white",
            relief=tk.SUNKEN,
            bd=2
        )
        self.canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # LEYENDA 
        leyenda_frame = ttk.Frame(main_frame)
        leyenda_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0))
        
        # Elementos de leyenda
        ttk.Label(leyenda_frame, text="●", font=("Arial", 14), 
                 foreground="blue").grid(row=0, column=0, padx=5)
        ttk.Label(leyenda_frame, text="Aeronave", 
                 font=("Arial", 9)).grid(row=0, column=1, padx=10)
        
        ttk.Label(leyenda_frame, text="●", font=("Arial", 14), 
                 foreground="red").grid(row=0, column=2, padx=5)
        ttk.Label(leyenda_frame, text="Aeronave en riesgo", 
                 font=("Arial", 9)).grid(row=0, column=3, padx=10)
        
        ttk.Label(leyenda_frame, text="――", font=("Arial", 14), 
                 foreground="red").grid(row=0, column=4, padx=5)
        ttk.Label(leyenda_frame, text="Riesgo de colisión", 
                 font=("Arial", 9)).grid(row=0, column=5, padx=10)
        
        ttk.Label(leyenda_frame, text="━━━", font=("Arial", 14), 
                 foreground="green").grid(row=0, column=6, padx=5)
        ttk.Label(leyenda_frame, text="Par más cercano", 
                 font=("Arial", 9)).grid(row=0, column=7, padx=10)
        
        # Información del algoritmo
        ttk.Label(main_frame, 
                 text="Algoritmo: Divide y Vencerás puro | Complejidad: O(n log n)",
                 font=("Arial", 9, "italic"),
                 foreground="gray").grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        # Dibujar mensaje inicial
        self.dibujar_mensaje_inicial()
    
    def dibujar_mensaje_inicial(self):
        """Dibuja mensaje de bienvenida en el canvas"""
        self.canvas.delete("all")
        
        # Fondo
        self.canvas.create_rectangle(0, 0, self.ancho_canvas, self.alto_canvas, 
                                    fill="#f0f8ff", outline="")
        
        # Título
        self.canvas.create_text(self.ancho_canvas/2, self.alto_canvas/2 - 50,
                               text="SISTEMA DE CONTROL AÉREO",
                               font=("Arial", 20, "bold"),
                               fill="navy")
        
        # Subtítulo
        self.canvas.create_text(self.ancho_canvas/2, self.alto_canvas/2 - 15,
                               text="Algoritmo Divide y Vencer",
                               font=("Arial", 14),
                               fill="darkblue")
        
        # Instrucciones
        instrucciones = [
            "1. Ingrese el número de aeronaves",
            "2. Establezca el umbral de distancia",
            "3. Haga clic en 'Generar'",
            "4. Luego en 'Analizar'",
            "",
            "El par más cercano se mostrará",
            "con línea verde gruesa",
            "y las demás con líneas rojas."
        ]
        
        y = self.alto_canvas/2 + 30
        for linea in instrucciones:
            self.canvas.create_text(self.ancho_canvas/2, y,
                                   text=linea,
                                   font=("Arial", 10),
                                   fill="gray")
            y += 25
    
    def convertir_coordenadas(self, punto: Aeronave) -> tuple:
        """Convierte coordenadas (0-100) a píxeles del canvas"""
        x_pixel = self.margen + (punto.x / 100) * (self.ancho_canvas - 2 * self.margen)
        y_pixel = self.alto_canvas - self.margen - (punto.y / 100) * (self.alto_canvas - 2 * self.margen)
        return x_pixel, y_pixel
    
    def generar_aeronaves(self):
        """Genera nuevas aeronaves aleatorias"""
        try:
            n = int(self.var_n.get())
            
            if n < 2:
                messagebox.showerror("Error", "Mínimo 2 aeronaves")
                return
            
            self.aeronaves = generar_aeronaves(n)
            self.pares_cercanos = []
            self.par_mas_cercano = None
            
            self.mostrar_resultado(f"Aeronaves generadas: {n}\nListo para analizar.")
            self.dibujar_escena()
            
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
    
    def analizar(self):
        """Ejecuta el algoritmo Divide y Vencer"""
        try:
            if not self.aeronaves:
                messagebox.showwarning("Atención", "Primero genere aeronaves")
                return
            
            umbral = float(self.var_umbral.get())
            
            if umbral <= 0:
                messagebox.showerror("Error", "Umbral debe ser > 0")
                return
            
            # EJECUTAR ALGORITMO DIVIDE Y VENCER
            self.pares_cercanos = encontrar_pares_cercanos(self.aeronaves, umbral)
            
            # Encontrar el par más cercano
            self.par_mas_cercano = encontrar_par_mas_cercano(self.pares_cercanos)
            
            # Mostrar resultados
            self.mostrar_resultados_completos(umbral)
            
            # Actualizar visualización
            self.dibujar_escena()
            
        except ValueError:
            messagebox.showerror("Error", "Umbral inválido")
    
    def mostrar_resultado(self, mensaje: str):
        """Muestra un mensaje simple"""
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(1.0, mensaje)
    
    def mostrar_resultados_completos(self, umbral: float):
        """Muestra resultados detallados del análisis"""
        texto = "=" * 40 + "\n"
        texto += "   ANÁLISIS COMPLETADO   \n"
        texto += "=" * 40 + "\n\n"
        
        texto += "RESULTADOS\n"
        texto += "―" * 20 + "\n"
        texto += f"Aeronaves: {len(self.aeronaves)}\n"
        texto += f"Umbral: {umbral:.2f}\n"
        texto += f"Pares cercanos encontrados: {len(self.pares_cercanos)}\n\n"
        
        if self.pares_cercanos:
            if self.par_mas_cercano:
                a, b = self.par_mas_cercano
                dist_min = distancia(a, b)
                texto += "PAR MÁS CERCANO \n"
                texto += "―" * 20 + "\n"
                texto += f"A: {a}\n"
                texto += f"B: {b}\n"
                texto += f"Distancia: {dist_min:.3f}\n\n"
            
            texto += "AERONAVES EN RIESGO \n"
            texto += "―" * 30 + "\n\n"
            
            # Ordenar por distancia
            pares_ordenados = sorted(self.pares_cercanos, 
                                   key=lambda p: distancia(p[0], p[1]))
            
            for i, (a, b) in enumerate(pares_ordenados, 1):
                dist = distancia(a, b)
                
                # Marcar el par más cercano con un indicador especial
                if (a, b) == self.par_mas_cercano or (b, a) == self.par_mas_cercano:
                    texto += f"Par {i} [MÁS CERCANO]:\n"
                else:
                    texto += f"Par {i}:\n"
                
                texto += f"  • A: {a}\n"
                texto += f"  • B: {b}\n"
                texto += f"  • Distancia: {dist:.3f}\n"
                
                if i < len(pares_ordenados):
                    texto += "  ―――――――――――――――――\n"
            
            texto += f"\nTotal de conexiones de riesgo: {len(self.pares_cercanos)}\n"
        else:
            texto += "TODAS LAS AERONAVES ESTÁN SEGURAS\n"
            texto += "No hay pares con distancia ≤ umbral\n"
        
        texto += "\n" + "=" * 40 + "\n"
        texto += "INFORMACIÓN DEL ALGORITMO\n"
        texto += "―" * 25 + "\n"
        texto += "• Técnica: Divide y Vencer\n"
        texto += "• Complejidad: O(n log n)\n"
        texto += "• Caso base: n ≤ 3\n"
        texto += "• Búsqueda en banda: O(n)\n"
        
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(1.0, texto)
    
    def dibujar_escena(self):
        """Dibuja todas las aeronaves y conexiones"""
        self.canvas.delete("all")
        
        # Dibujar cuadrícula
        self.dibujar_cuadricula()
        
        # Dibujar aeronaves
        for aeronave in self.aeronaves:
            x, y = self.convertir_coordenadas(aeronave)
            
            # Verificar si esta aeronave está en algún par cercano
            en_riesgo = any(aeronave in par for par in self.pares_cercanos)
            
            if en_riesgo:
                # Aeronave en riesgo
                self.canvas.create_oval(x-7, y-7, x+7, y+7,
                                       fill="#ffcccc", outline="red", width=2)
            else:
                # Aeronave segura
                self.canvas.create_oval(x-5, y-5, x+5, y+5,
                                       fill="blue", outline="darkblue", width=1)
            
            # Etiqueta para pocas aeronaves
            if len(self.aeronaves) <= 50:
                self.canvas.create_text(x, y-12,
                                       text=f"({aeronave.x:.0f},{aeronave.y:.0f})",
                                       font=("Arial", 7))
        
        # Primero dibujar todas las conexiones rojas (excepto el par más cercano si existe)
        for a, b in self.pares_cercanos:
            if self.par_mas_cercano and ((a, b) == self.par_mas_cercano or (b, a) == self.par_mas_cercano):
                continue  # Saltar el par más cercano para dibujarlo después
                
            x1, y1 = self.convertir_coordenadas(a)
            x2, y2 = self.convertir_coordenadas(b)
            
            # Línea roja normal
            self.canvas.create_line(x1, y1, x2, y2,
                                   fill="red", width=2)
            
            # Distancia en el punto medio
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dist = distancia(a, b)
            
            self.canvas.create_text(mx, my-10,
                                   text=f"{dist:.1f}",
                                   font=("Arial", 8),
                                   fill="darkred")
        
        # Dibujar el par más cercano en verde (si existe)
        if self.par_mas_cercano:
            a, b = self.par_mas_cercano
            x1, y1 = self.convertir_coordenadas(a)
            x2, y2 = self.convertir_coordenadas(b)
            
            # Línea verde gruesa para el par más cercano
            self.canvas.create_line(x1, y1, x2, y2,
                                   fill="green", width=4, dash=(5, 2))
            
            # Resaltar las aeronaves del par más cercano
            self.canvas.create_oval(x1-8, y1-8, x1+8, y1+8,
                                   outline="green", width=3)
            self.canvas.create_oval(x2-8, y2-8, x2+8, y2+8,
                                   outline="green", width=3)
            
            # Distancia en el punto medio con fondo
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dist = distancia(a, b)
            
            # Fondo para el texto
            self.canvas.create_rectangle(mx-25, my-20, mx+25, my+5,
                                        fill="white", outline="green", width=2)
            
            self.canvas.create_text(mx, my-7,
                                   text=f"{dist:.1f}",
                                   font=("Arial", 9, "bold"),
                                   fill="darkgreen")
            
            # Etiqueta "MÁS CERCANO"
            self.canvas.create_text(mx, my+15,
                                   text="MÁS CERCANO",
                                   font=("Arial", 8, "bold"),
                                   fill="darkgreen")
        
        # Dibujar ejes
        self.dibujar_ejes()
    
    def dibujar_cuadricula(self):
        """Dibuja cuadrícula de referencia"""
        # Vertical
        for i in range(0, 101, 10):
            x = self.margen + (i / 100) * (self.ancho_canvas - 2 * self.margen)
            self.canvas.create_line(x, self.margen, x, self.alto_canvas - self.margen,
                                   fill="#e8e8e8", width=1)
            
            if i % 20 == 0:
                self.canvas.create_text(x, self.alto_canvas - self.margen + 15,
                                       text=str(i), font=("Arial", 8))
        
        # Horizontal
        for i in range(0, 101, 10):
            y = self.alto_canvas - self.margen - (i / 100) * (self.alto_canvas - 2 * self.margen)
            self.canvas.create_line(self.margen, y, self.ancho_canvas - self.margen, y,
                                   fill="#e8e8e8", width=1)
            
            if i % 20 == 0:
                self.canvas.create_text(self.margen - 15, y,
                                       text=str(i), font=("Arial", 8))
    
    def dibujar_ejes(self):
        """Dibuja ejes X e Y"""
        # Eje X
        self.canvas.create_line(self.margen, self.alto_canvas - self.margen,
                               self.ancho_canvas - self.margen, self.alto_canvas - self.margen,
                               fill="black", width=2)
        
        # Eje Y
        self.canvas.create_line(self.margen, self.margen,
                               self.margen, self.alto_canvas - self.margen,
                               fill="black", width=2)
        
        # Etiquetas
        self.canvas.create_text(self.ancho_canvas - self.margen + 20,
                               self.alto_canvas - self.margen,
                               text="X", font=("Arial", 10, "bold"))
        
        self.canvas.create_text(self.margen, self.margen - 20,
                               text="Y", font=("Arial", 10, "bold"))
    
    def limpiar(self):
        """Limpia toda la simulación"""
        self.canvas.delete("all")
        self.aeronaves = []
        self.pares_cercanos = []
        self.par_mas_cercano = None
        self.texto_resultados.delete(1.0, tk.END)
        self.dibujar_mensaje_inicial()

# EJECUCIÓN PRINCIPAL


def main():
    """Función principal"""
    ventana = tk.Tk()
    app = SistemaControlAereo(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()