// Definición de pines para el sensor TCS3200/TCS230
#define S0 8  // Pin de entrada para seleccionar la escala de frecuencia
#define S1 9  // Pin de entrada para seleccionar la escala de frecuencia
#define S2 10 // Pin de entrada para seleccionar el filtro de color
#define S3 11 // Pin de entrada para seleccionar el filtro de color
#define outPin 4 // Pin de salida de frecuencia (conectado al pin digital 4)

// Variables para almacenar los valores de frecuencia de cada color
int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;
// En algunos proyectos se utiliza un cuarto color 'clear' (sin filtro)
int clearFrequency = 0;

void setup() {
  // Inicializa la comunicación serial
  Serial.begin(9600);
  Serial.println("Iniciando prueba del Sensor de Color TCS3200...");
  
  // Configura los pines del sensor como salidas
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  
  // Configura el pin de salida como entrada para la lectura de la frecuencia
  pinMode(outPin, INPUT);
  
  // Configura la escala de frecuencia al 20% (S0=HIGH, S1=LOW)
  // 0% -> LOW/LOW, 2% -> LOW/HIGH, 20% -> HIGH/LOW, 100% -> HIGH/HIGH
  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);
  
  // Espera un momento para que el sensor se estabilice
  delay(100); 
}

void loop() {
  // 1. **Leer la Frecuencia del Color ROJO** (S2=LOW, S3=LOW)
  digitalWrite(S2, LOW);
  digitalWrite(S3, LOW);
  // Usa pulseIn() para medir la duración de un pulso, lo cual se relaciona con la frecuencia.
  // Es una forma de leer la frecuencia.
  redFrequency = pulseIn(outPin, LOW); 
  
  // 2. **Leer la Frecuencia del Color VERDE** (S2=HIGH, S3=HIGH)
  digitalWrite(S2, HIGH);
  digitalWrite(S3, HIGH);
  greenFrequency = pulseIn(outPin, LOW);
  
  // 3. **Leer la Frecuencia del Color AZUL** (S2=LOW, S3=HIGH)
  digitalWrite(S2, LOW);
  digitalWrite(S3, HIGH);
  blueFrequency = pulseIn(outPin, LOW);
  
  // Opcional: Leer la Frecuencia sin Filtro (Clear) (S2=HIGH, S3=LOW)
  /*
  digitalWrite(S2, HIGH);
  digitalWrite(S3, LOW);
  clearFrequency = pulseIn(outPin, LOW);
  */
  
  // 4. **Imprimir los resultados en el Monitor Serial**
  Serial.print("Rojo: ");
  Serial.print(redFrequency);
  Serial.print(" | Verde: ");
  Serial.print(greenFrequency);
  Serial.print(" | Azul: ");
  Serial.print(blueFrequency);
  /*
  Serial.print(" | Clear: ");
  Serial.print(clearFrequency);
  */
  Serial.println();
  
  // Esperar un breve momento antes de la próxima lectura
  delay(500); 
}