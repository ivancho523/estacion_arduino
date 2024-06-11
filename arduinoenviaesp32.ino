#include <Wire.h>
#include <DHT.h>
#include <DFRobot_OzoneSensor.h>
#include <SoftwareSerial.h>

#define COLLECT_NUMBER 20
#define Ozone_IICAddress OZONE_ADDRESS_3
#define DHTPIN 2  // El pin al que está conectado el sensor DHT11
#define DHTTYPE DHT11  // Tipo de sensor DHT

DFRobot_OzoneSensor Ozone;
DHT dht(DHTPIN, DHTTYPE);
int sensorIn = A0;

// Configura SoftwareSerial en los pines 5 (RX) y 6 (TX)
SoftwareSerial espSerial(5, 6);

void setup() {
  Serial.begin(9600); // Comunicación con el monitor serial
  espSerial.begin(115200); // Comunicación con el ESP32
  dht.begin();

  Serial.println("Inicializando sensor de ozono...");
  while (!Ozone.begin(Ozone_IICAddress)) {
    Serial.println("Error al conectar con el sensor de ozono a través de I2C!");
    delay(1000);
  }
  Serial.println("Conexión I2C exitosa!");
}

void loop() {
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();
  int ozono = Ozone.readOzoneData(COLLECT_NUMBER);
  int co = analogRead(A4); 
  int co2 = analogRead(sensorIn);

  // Enviar los datos como una cadena CSV al ESP32
  String data = String(temperatura) + ";" + String(humedad) + ";" + String(ozono) + ";" + String(co) + ";" + String(co2);
  Serial.println(data);
  espSerial.println(data);

  // Enviar datos al monitor serial para depuración
  Serial.println("Enviando datos al ESP32: " + data);

  delay(60000); // Esperar 3 segundos antes de tomar la siguiente lectura
}


