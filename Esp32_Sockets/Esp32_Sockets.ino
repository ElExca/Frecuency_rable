#include <ArduinoWebsockets.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP085.h"
#include <WiFi.h>
#include <ArduinoJson.h>
#include <FirebaseESP32.h>
#include <DHT.h>
#include <Wire.h>

const char* ssid = "ssid"; // Ingresa el SSID
const char* password = "contrasenia"; // Ingresa la contraseña
const char* websockets_server_host = "ip host"; // Ingresa la dirección del servidor
const uint16_t websockets_server_port = 5000; // Ingresa el puerto del servidor
#define FIREBASE_HOST "direccion"
#define FIREBASE_AUTH "codigo de auth"

String ruta = "Data-sensors";

#define DHTPIN 23          // Pin del sensor DHT22
#define DHTTYPE DHT22     // Tipo de sensor DHT (DHT11 o DHT22)

FirebaseData firebaseData;
DHT dht(DHTPIN, DHTTYPE,22); // Inicializar el objeto DHT
Adafruit_BMP085 bmp;


#define MQ7_PIN A4   //Pin analogico de mq7

using namespace websockets;

WebsocketsClient client;
void reconnect() {
  Serial.println("Intentando reconectar al servidor WebSocket...");
  if (client.connect(websockets_server_host, websockets_server_port, "/")) {
    Serial.println("Conexión WebSocket restablecida");
  } else {
    Serial.println("Error al conectar al servidor WebSocket");
  }
}


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
  //Inicializar el sensor bmp
  bmp.begin();
  // Conectar al servidor WebSocket
  Serial.println("Conectando al servidor WebSocket...");
  if (client.connect(websockets_server_host, websockets_server_port, "/")) {
    Serial.println("Conexión WebSocket establecida");
  } else {
    Serial.println("Error al conectar al servidor WebSocket");
  }
    // Inicializar Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
}

void loop() {
    client.poll();

  // Verificar si la conexión WebSocket está abierta
  if (!client.available()) {
    reconnect(); // Intentar reconexión si no está disponible
  }
  
  // Leer temperatura y humedad del sensor DHT22
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int CO2 = analogRead(MQ7_PIN);
  float pressure = bmp.readPressure();
  float altitude = bmp.readAltitude();

  temperature = round(temperature * 100) / 100;
  humidity = round(humidity * 100) / 100;
  CO2 = round(CO2 * 100) / 100;
  pressure = round(pressure * 100) / 100;
  altitude = round(altitude * 100) / 100;



  // Crear un objeto JSON y asignar los valores de temperatura y humedad
  DynamicJsonDocument jsonDocument(256);
  jsonDocument["Humidity"] = humidity;
  jsonDocument["Temperature"] = temperature;
  jsonDocument["CO2"] = CO2;
  jsonDocument["Pressure"] = pressure;
  jsonDocument["Altitude"] = altitude;


  // Serializar el objeto JSON en una cadena
  String jsonData;
  serializeJson(jsonDocument, jsonData);

  // Enviar la cadena JSON al servidor WebSocket
    if (client.available()) {
    client.send(jsonData);
  }
  delay(5000);

  Firebase.setInt(firebaseData,ruta+ "/Temperatura",temperature);
  Firebase.setInt(firebaseData,ruta+ "/Pressure",pressure);
  Firebase.setInt(firebaseData,ruta+ "/Humidity",humidity);
  Firebase.setInt(firebaseData,ruta+ "/Altitude",altitude);
  Firebase.setInt(firebaseData,ruta+ "/CO2",CO2);
  delay(2000);

  

  // Esperar un momento antes de enviar el siguiente dato
  
}
