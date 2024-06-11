#include <Wire.h>
#include <DHT.h>
#include <DFRobot_OzoneSensor.h>
#include <SoftwareSerial.h>

#define COLLECT_NUMBER 20
#define Ozone_IICAddress OZONE_ADDRESS_3
#define DHTPIN 2  // El pin al que está conectado el sensor DHT11
#define DHTTYPE DHT11  // Tipo de sensor DHT
#define CO_PIN A0  // Pin analógico donde está conectado el sensor de CO

DFRobot_OzoneSensor Ozone;
DHT dht(DHTPIN, DHTTYPE);

// Configura SoftwareSerial en los pines 5 (RX) y 6 (TX) para la comunicación con el ESP32
SoftwareSerial espSerial(5, 6);
// Configura SoftwareSerial en los pines 10 (RX) y 11 (TX) para el sensor de CO2
SoftwareSerial co2Serial(10, 11);

unsigned char hexdata[9] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79}; // Comando de lectura de densidad de gas

void setup() {
  Serial.begin(9600); // Comunicación con el monitor serial
  espSerial.begin(115200); // Comunicación con el ESP32
  co2Serial.begin(9600); // Comunicación con el sensor de CO2
  dht.begin();

  Serial.println("Inicializando sensor de ozono...");
  while (!Ozone.begin(Ozone_IICAddress)) {
    Serial.println("Error al conectar con el sensor de ozono a través de I2C!");
    delay(1000);
  }
  Serial.println("Conexión I2C exitosa!");
}

void loop() {
  // Leer datos del sensor DHT11
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();
  int ozono = Ozone.readOzoneData(COLLECT_NUMBER);

  // Leer datos del sensor de CO2
  co2Serial.write(hexdata, 9);
  delay(500);

  long co2_concentration = -1;
  long hi = 0;
  long lo = 0;
  
  for (int i = 0; i < 9; i++) {
    if (co2Serial.available() > 0) {
      int ch = co2Serial.read();
      if (i == 2) {
        hi = ch;   // Concentración alta
      }
      if (i == 3) {
        lo = ch;   // Concentración baja
      }
      if (i == 8) {
        co2_concentration = hi * 256 + lo;  // Concentración de CO2
      }
    }
  }

  // Leer datos del sensor de CO
  int co_val = analogRead(CO_PIN);

  // Enviar los datos como una cadena CSV al ESP32
  String data = String(temperatura) + ";" + String(humedad) + ";" + String(ozono) + ";" + String(co_val) + ";" + String(co2_concentration) + ";";
  espSerial.println(data);

  // Enviar datos al monitor serial para depuración
  Serial.println("Enviando datos al ESP32: " + data);

  delay(3000); // Esperar 3 segundos antes de tomar la siguiente lectura
}


