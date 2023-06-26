#include "DHT.h"
#include <ArduinoJson.h>
#define pin 21

DHT dht(pin, DHT11);

void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
 dht.begin();

}

void loop() {

  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();

  // Crear un objeto JSON
  DynamicJsonDocument jsonDocument(200);
  jsonDocument["temperatura"] = temperatura;
  jsonDocument["humedad"] = humedad;

  // Convertir el objeto JSON en una cadena JSON
  String jsonString;
  serializeJson(jsonDocument, jsonString);

  // Enviar la cadena JSON a través del puerto serie
  Serial.println(jsonString);

  delay(5000);


}