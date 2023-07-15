#include <ArduinoWebsockets.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP085.h"
#include <WiFi.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <FirebaseESP32.h>
#include <Wire.h>

const char* ssid = "ssid"; // Ingresa el SSID
const char* password = "contrasenia"; // Ingresa la contraseña
const char* websockets_server_host = "ip"; // Ingresa la dirección del servidor
const uint16_t websockets_server_port = 5000; // Ingresa el puerto del servidor

#define DHTPIN 27          // Pin del sensor DHT22
#define DHTTYPE DHT22     // Tipo de sensor DHT (DHT11 o DHT22)
//Firebase
#define FIREBASE_HOST "your-firebase-host.firebaseio.com" 
#define FIREBASE_AUTH "your-firebase-auth-token"

DHT dht(DHTPIN, DHTTYPE,22); // Inicializar el objeto DHT
Adafruit_BMP085 bmp;
FirebaseData firebaseData;

#define MQ7_PIN A4   //Pin analogico de mq7

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
  //Inicializar el sensor bmp
  bmp.begin();
    // Inicializar Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
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
  int c02 = analogRead(MQ7_PIN);
  float presion = bmp.readPressure();
  float altitud = bmp.readAltitude();

  // Crear un objeto JSON y asignar los valores de temperatura y humedad
  DynamicJsonDocument jsonDocument(256);
  jsonDocument["humidity"] = humidity;
  jsonDocument["temperature"] = temperature;
  jsonDocument["C02"] = c02;
  jsonDocument["pressure"] = presion;
  jsonDocument["altitude"] = altitud;


  // Serializar el objeto JSON en una cadena
  String jsonData;
  serializeJson(jsonDocument, jsonData);

  // Enviar la cadena JSON al servidor WebSocket
  client.send(jsonData);
  delay(5000);

    if (Firebase.pushString(firebaseData, "/sensor-data", jsonData)) {
    Serial.println("Datos enviados a Firebase");
  } else {
    Serial.println("Error al enviar los datos a Firebase");
    Serial.println(firebaseData.errorReason());
  }
  delay(2000);

  // Esperar un momento antes de enviar el siguiente dato
  
}
