#include <ArduinoWebsockets.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <DHT.h>

const char* ssid = "ssid"; // Ingresa el SSID
const char* password = "password"; // Ingresa la contraseña
const char* websockets_server_host = "ip_host"; // Ingresa la dirección del servidor
const uint16_t websockets_server_port = 5000; // Ingresa el puerto del servidor

#define DHTPIN 27          // Pin del sensor DHT22
#define DHTTYPE DHT22     // Tipo de sensor DHT (DHT11 o DHT22)

DHT dht(DHTPIN, DHTTYPE,22); // Inicializar el objeto DHT

using namespace websockets;

WebsocketsClient client;

void setup() {
  Serial.begin(115200);
  
  // Conexión a la red WiFi
  WiFi.begin(ssid, password);

  // Esperar a que se conecte a la red WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Conectado a la red WiFi");

  // Inicializar el sensor DHT22
  dht.begin();

  // Conectar al servidor WebSocket
  Serial.println("Conectando al servidor WebSocket...");
  if (client.connect(websockets_server_host, websockets_server_port, "/")) {
    Serial.println("Conexión WebSocket establecida");
  } else {
    Serial.println("Error al conectar al servidor WebSocket");
  }
}

void loop() {
  // Leer temperatura y humedad del sensor DHT22
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Crear un objeto JSON y asignar los valores de temperatura y humedad
  DynamicJsonDocument jsonDocument(256);
  jsonDocument["humidity"] = humidity;
  jsonDocument["temperature"] = temperature;

  // Serializar el objeto JSON en una cadena
  String jsonData;
  serializeJson(jsonDocument, jsonData);

  // Enviar la cadena JSON al servidor WebSocket
  client.send(jsonData);

  // Esperar un momento antes de enviar el siguiente dato
  delay(2000);
}
