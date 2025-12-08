
# **Sistema de Detección de Colisiones Aéreas**

**Proyecto Final - Análisis y Diseño de Algoritmos**  
**Ingeniería de Sistemas - Universidad del Valle (2025-II)**

## **Descripción General**

El seguimiento y supervisión de aeronaves en los sistemas modernos de control de tráfico aéreo es crucial para garantizar la seguridad en los espacios aéreos. Para lograrlo, los sistemas de radar procesan constantemente las coordenadas geográficas de las aeronaves, detectando posibles riesgos de colisión. Sin embargo, uno de los mayores desafíos es identificar, en tiempo real, las aeronaves que están a distancias mínimas entre sí, y determinar si existe un riesgo de colisión.

Este proyecto busca simular un sistema de control aéreo simplificado, basado en un plano cartesiano, para detectar de manera eficiente los pares de aeronaves más cercanas. Utilizando el algoritmo **Divide y Vencer**, se identifica de manera óptima los pares de aeronaves que representan un riesgo de colisión. Este algoritmo permite descomponer el problema en subproblemas más pequeños, resolverlos recursivamente, y luego combinar los resultados parciales para obtener la solución global.

## **Objetivo del Proyecto**

El objetivo del proyecto es diseñar e implementar una solución que utilice la técnica de **Dividir y Vencer** para encontrar los pares de aeronaves más cercanos en un espacio aéreo representado por un plano cartesiano. A través de este enfoque, se debe ser capaz de identificar y visualizar las aeronaves en riesgo de colisión.

### **Fases del Algoritmo:**

1. **Dividir**: El conjunto de aeronaves (puntos en el plano cartesiano) se divide en subgrupos más pequeños para facilitar el procesamiento.
   
2. **Conquistar**: Cada subgrupo se procesa recursivamente, utilizando el algoritmo para calcular las distancias entre las aeronaves y encontrar los pares más cercanos.
   
3. **Combinar**: Los resultados parciales de los subgrupos se combinan para obtener los pares más cercanos en el conjunto completo de aeronaves.

## **Requerimientos del Proyecto**

### **1. Planteamiento Teórico y Análisis Algorítmico**
El primer componente de este proyecto se enfoca en la descripción teórica del problema. Esto incluye:

- **Descripción formal del problema**: Explicación detallada de la situación y el objetivo del sistema de control aéreo.
- **Justificación del uso de la técnica de Dividir y Vencer**: Razón por la cual se utiliza este enfoque algorítmico y cómo contribuye a una solución eficiente.
- **Análisis de complejidad temporal y espacial**: Estudio de la eficiencia del algoritmo en términos de tiempo y espacio, explicando la complejidad **O(n log n)** de la técnica de **Dividir y Vencer**.

### **2. Implementación**
La segunda parte del proyecto se basa en la implementación del algoritmo en Python, siguiendo los principios de la técnica de **Dividir y Vencer**. Los componentes clave son:

- **Generación aleatoria de aeronaves**: El sistema debe generar **n** aeronaves con coordenadas aleatorias dentro de un rango definido (0-100 para las coordenadas X y Y).
- **Cálculo de las distancias**: El algoritmo debe calcular la distancia euclidiana entre cada par de aeronaves y determinar si están dentro del umbral de riesgo de colisión.
- **Uso de clases y estructuras de datos adecuadas**: El código emplea clases y estructuras como listas, tuplas y vectores para almacenar y gestionar las aeronaves y los pares cercanos.

### **3. Interfaz Visual**
El sistema debe contar con una **interfaz gráfica de usuario (GUI)** para representar las aeronaves y los pares cercanos en el plano cartesiano. Los puntos generados deben ser visibles, y se debe resaltar el par o los pares más cercanos utilizando líneas de diferentes colores. La visualización incluye:

- **Representación gráfica de las aeronaves**: Cada aeronave se representa como un punto en el plano cartesiano, con coordenadas generadas aleatoriamente.
- **Resaltado visual de los pares cercanos**: Se destaca el par más cercano con una línea verde gruesa y los demás pares de aeronaves con líneas rojas, indicando el riesgo de colisión.
- **Cuadricula y ejes**: Se dibuja una cuadrícula de referencia para facilitar la visualización y los ejes X y Y para indicar las coordenadas de cada aeronave.
- **Resultados en texto**: El sistema muestra información sobre los pares cercanos y la distancia entre ellos.

## **Tecnologías Utilizadas**

Este proyecto se ha implementado utilizando las siguientes tecnologías:

- **Python 3.x**: Lenguaje de programación principal para implementar la solución algorítmica y la interfaz gráfica.
- **Tkinter**: Librería estándar de Python para la creación de la interfaz gráfica de usuario (GUI).
- **Matplotlib (opcional)**: Para mejorar la visualización gráfica de los puntos y las distancias, si se decide usarla para generar gráficos adicionales.
  
## **Estructura del Proyecto**

El código fuente del proyecto está organizado de la siguiente manera:

### **1. Clases y Funciones**
- **Aeronave**: Clase que representa una aeronave en el espacio aéreo. Cada aeronave tiene un par de coordenadas (X, Y) generadas aleatoriamente.
- **Distancia**: Función que calcula la distancia euclidiana entre dos aeronaves.
- **Dividir y Vencer**: Implementación de la técnica **Dividir y Vencer** para encontrar los pares de aeronaves más cercanos.
- **Generación de aeronaves**: Función que genera **n** aeronaves de forma aleatoria dentro de un rango definido.

### **2. Interfaz Gráfica**
- **SistemaControlAereo**: La clase principal que gestiona la interfaz gráfica, permite la interacción con el usuario, muestra los resultados y visualiza la simulación.

## **Instrucciones para Ejecutar el Proyecto**

Para ejecutar el proyecto en tu máquina, sigue estos pasos:

1. **Instalar Python**: Asegúrate de tener Python 3.x instalado. Si no lo tienes, puedes descargarlo desde [python.org](https://www.python.org/downloads/).

2. **Instalar las dependencias necesarias**:
   - Tkinter ya viene preinstalado con Python, pero asegúrate de tenerlo disponible. Si no, puedes instalarlo mediante:
     ```bash
     pip install tkinter
     ```

3. **Ejecutar el Programa**:
   - Descarga el archivo del proyecto y navega hasta la carpeta del proyecto en tu terminal o explorador de archivos.
   - Ejecuta el archivo principal `proyecto.py`:

     ```bash
     python proyecto.py
     ```

4. **Interacción con la Interfaz**:
   - En la interfaz, podrás ingresar el número de aeronaves y el umbral de distancia.
   - Haz clic en el botón "Generar" para generar las aeronaves aleatorias y luego en "Analizar" para ejecutar el algoritmo y mostrar los resultados.

## **Resultados Esperados**

Al ejecutar el proyecto, deberías obtener los siguientes resultados:

1. **Generación de aeronaves**: El sistema genera un número de aeronaves aleatorias dentro del rango definido (0-100 en ambos ejes).
2. **Visualización de los pares cercanos**: Los pares de aeronaves más cercanas se destacan con líneas rojas, mientras que el par más cercano (si lo hay) se resalta con una línea verde gruesa.
3. **Información detallada**: El sistema muestra información detallada sobre las aeronaves generadas, las distancias entre ellas, y si existe algún riesgo de colisión.

## **Conclusión**

Este proyecto presenta una solución efectiva para la detección de posibles colisiones aéreas utilizando el algoritmo **Dividir y Vencer**. La implementación no solo optimiza el proceso de cálculo de los pares más cercanos mediante la técnica algorítmica, sino que también ofrece una visualización clara y útil de los riesgos potenciales. La interfaz gráfica facilita la interacción con el sistema, y los resultados se presentan de forma detallada para facilitar su interpretación.
