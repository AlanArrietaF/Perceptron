# Clasificador de Frutas (Perceptrón & Arduino)

Un sistema de clasificación de hardware y software que utiliza un sensor de color físico para distinguir entre manzanas y limones. El proyecto integra la captura de datos en tiempo real mediante un microcontrolador y el procesamiento analítico de estos datos utilizando un modelo de Perceptrón en Python.

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.x, C++ (Arduino)
* **Hardware:** Placa Arduino (UNO/Nano), Sensor de Color TCS3200
* **Manipulación de Datos:** Pandas, NumPy
* **Modelo de Machine Learning:** Scikit-Learn (o implementación directa en Python)
* **Formatos de Archivo:** CSV

## Arquitectura Técnica Destacada

El desarrollo de este proyecto aborda la integración de señales físicas con la lógica matemática de las redes neuronales:

### 1. Sistema de Captura y Calibración (Hardware)
El hardware está controlado por el script `calibracion.ino`, el cual gestiona el sensor TCS3200.
* **Muestreo de Frecuencias:** El microcontrolador lee las señales cuadradas generadas por los fotodiodos del sensor, filtrando independientemente los canales de luz (Rojo, Verde, Azul).
* **Calibración Ambiental:** El código integra una etapa de calibración para establecer los niveles de "blanco" y "negro", normalizando las lecturas según las condiciones de iluminación reales del entorno antes de extraer los datos.

### 2. Generación de Datasets Personalizados
Para resolver problemas de confianza estadística e incompatibilidades que surgen al usar bases de datos externas, el proyecto emplea un enfoque de recolección de datos primarios.
* **Estructura CSV:** Los datos extraídos en la fase de calibración se tabulan en `manzanas.csv` y `limones.csv`. Al capturar los datos manualmente, el modelo se entrena con proporciones de color altamente específicas al entorno de prueba, eliminando el ruido de datos ajenos.

### 3. Modelo de Clasificación Binaria
El archivo `perceptron.py` actúa como el motor de toma de decisiones.
* **Preprocesamiento:** Utilización de DataFrames (`pandas`) para unificar los CSVs, limpiar los datos y estructurarlos en una matriz de características (Features) y etiquetas (Labels).
* **Entrenamiento:** Implementación de un Perceptrón multicapa o de capa simple. Durante las épocas de entrenamiento, el algoritmo ajusta sus pesos sinápticos basándose en los errores de predicción, buscando el hiperplano óptimo que separe linealmente el espacio de color de una manzana del de un limón.

### 4. Lógica de Activación
La predicción final se calcula mediante la suma ponderada de las frecuencias RGB recibidas. Si el valor de salida cruza el umbral de la función de activación configurada en la neurona, el sistema clasifica de forma determinista la muestra analizada.

## Cómo Ejecutar el Proyecto

1.  Asegúrate de tener instaladas las dependencias de Python necesarias:
    ```bash
    pip install pandas numpy scikit-learn
    ```
2.  Conecta el sensor TCS3200 a la placa Arduino respetando la declaración de pines en el archivo `calibracion.ino`.
3.  Compila y sube el código `.ino` a tu placa utilizando el Arduino IDE para verificar la calibración en el Monitor Serie.
4.  Coloca los archivos `manzanas.csv`, `limones.csv` y `perceptron.py` en un mismo directorio.
5.  Ejecuta el entrenamiento y clasificación desde la terminal:
    ```bash
    python perceptron.py
    ```

## Ejemplo de Datos (CSV)

```text
R,G,B,Clase
120,45,30,manzana
135,50,38,manzana
80,140,40,limon
75,138,45,limon
...
```
