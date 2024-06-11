#include <WiFi.h>
#include <PubSubClient.h>

// Configuración de la red WiFi
const char* ssid = "Redmi Note 10S";
const char* password = "compartido";

// Configuración del servidor MQTT
const char* mqtt_server = "165.227.126.203";  // Dirección IP del servidor MQTT
const int mqtt_port = 1883; // Puerto MQTT

// Tema MQTT
const char* mqtt_topic = "datos_estacion";  // Tema MQTT al que se enviarán los datos

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Conectado a la red WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Intentando conexión MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado al servidor MQTT");
    } else {
      Serial.print("falló, rc=");
      Serial.print(client.state());
      Serial.println(" Intentando de nuevo en 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  Serial2.begin(115200, SERIAL_8N1, 17, 16); // Comunicación con el Arduino
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  // Verificar si hay datos disponibles en el puerto serial
  if (Serial2.available() > 0) {
    String data = Serial2.readStringUntil('\n'); // Leer datos hasta un salto de línea
    data.trim(); // Eliminar espacios en blanco iniciales y finales

    // Verificar que los datos no estén vacíos
    if (data.length() > 0) {
      // Publicar datos en el tema MQTT
      if (client.publish(mqtt_topic, data.c_str())) {
        Serial.println("Datos publicados en el servidor MQTT: " + data);
      } else {
        Serial.println("Error al publicar los datos en el servidor MQTT");
      }
    }
  }

  client.loop(); // Necesario para mantener la conexión MQTT activa
  delay(1000);  // Esperar 1 segundo antes de revisar nuevamente
}



