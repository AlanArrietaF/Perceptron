import numpy as np
import pandas as pd
import serial # Necesario para la comunicación serial
import time   # Necesario para el retardo en la conexión
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split 
from pandas.errors import EmptyDataError 

# --- Configuración del Puerto Serial ---
# Cambia 'COM3' (Windows) o '/dev/ttyUSB0' (Linux/Mac)
# y 9600 a los valores que uses en tu Arduino.
PORT_SERIAL = '/dev/ttyACM0'  
BAUD_RATE = 9600

# 1. --- Cargar y Preparar los Datos (Mismo código anterior) ---
try:
    df_manzanas = pd.read_csv('manzanas.csv', header=0) 
    df_manzanas['Clase'] = 1 
    df_limones = pd.read_csv('limones.csv', header=0)
    df_limones['Clase'] = 0 
    
except FileNotFoundError:
    print("Error: Asegúrate de que los archivos 'manzanas.csv' y 'limones.csv' están en el directorio correcto.")
    exit()
except EmptyDataError:
    print("Error: Uno de los archivos CSV está vacío. Por favor, revisa su contenido.")
    exit()
    
df_completo = pd.concat([df_manzanas, df_limones], ignore_index=True)
p = df_completo[['R', 'G', 'B']].values 
a = df_completo['Clase'].values 
p_train, p_test, a_train, a_test = train_test_split(p, a, test_size=0.2, random_state=42)


# 2. --- Entrenar el MLP ---
mlp = MLPClassifier(hidden_layer_sizes=(3, 3), max_iter=400, random_state=42)
print("Iniciando entrenamiento...")
mlp.fit(p_train, a_train)
print("Entrenamiento finalizado.")


# 3. --- Conexión y Lectura de Arduino ---

try:
    # 3.1 Inicializar la conexión serial
    print(f"Conectando a Arduino en {PORT_SERIAL}...")
    ser = serial.Serial(PORT_SERIAL, BAUD_RATE)
    time.sleep(2) # Esperar un momento para establecer la conexión

    # 3.2 Leer datos del sensor RGB
    print("\nEsperando datos del sensor RGB... (Envía 'R,G,B' desde Arduino)")
    
    # Leer la línea completa de datos
    linea = ser.readline().decode('utf-8').strip()
    
    # 3.3 Procesar los datos
    r, g, b = map(float, linea.split(','))
    
    # La red neuronal espera una matriz de 2 dimensiones, de ahí el [[]]
    datos_sensor = np.array([[r, g, b]])
    
    print(f"Datos RGB recibidos: R={r:.3f}, G={g:.3f}, B={b:.3f}")

    # 3.4 Predicción
    prediccion = mlp.predict(datos_sensor)[0]
    
    if prediccion == 1:
        resultado_str = "MANZANA"
    else:
        resultado_str = "LIMÓN"
        
    print("\n" + "="*50)
    print("## ✅ RESULTADO DE LA CLASIFICACIÓN")
    print(f"La muestra es: {resultado_str} (Clase: {prediccion:.0f})")
    print("="*50)


    # 4. --- Imprimir Parámetros Solicitados ---
    print("\n## Parámetros Utilizados")
    
    # Último Peso (entre la penúltima capa oculta y la capa de salida)
    # Es el último elemento de la lista mlp.coefs_
    ultimo_peso = mlp.coefs_[-1]
    print(f"\nÚLTIMO PESO UTILIZADO (Shape: {ultimo_peso.shape}):")
    print(ultimo_peso)
    
    # Último Sesgo (aplicado a la capa de salida)
    # Es el último elemento de la lista mlp.intercepts_
    ultimo_bias = mlp.intercepts_[-1]
    print(f"\nÚLTIMO BIAS UTILIZADO (Shape: {ultimo_bias.shape}):")
    print(ultimo_bias)
    
    print("="*50)
    
except serial.SerialException as e:
    print(f"\n❌ Error de conexión serial: {e}")
    print(f"Asegúrate de que Arduino está conectado al puerto {PORT_SERIAL} y el script tiene permiso para acceder a él.")
except Exception as e:
    print(f"\n❌ Error durante el proceso: {e}")

finally:
    # 5. --- Cerrar la conexión serial ---
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("\nConexión serial cerrada.")
