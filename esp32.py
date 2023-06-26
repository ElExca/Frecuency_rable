import serial
import json
from pymongo import MongoClient
# URL de conexión a MongoDB (asegúrate de reemplazar los valores por los correctos)
class DB:
    def connectDB(self):

        client = MongoClient("mongodb://127.0.0.1:27017/")
        database = client["Esp32"]
        collection = database["Datos"]

        return collection

class ESP32_reading:

    def reading_esp32(self):
        ser = serial.Serial('COM6', 9600)
        connect = DB()
        while True:
            if ser.in_waiting > 0:
                # Leer la cadena JSON del puerto serie
                data = ser.readline().decode('utf-8').rstrip()

                # Analizar la cadena JSON
                json_data = json.loads(data)
                self.temperatura = json_data['temperatura']

                json_data = {
                    "Temperatura": json_data['temperatura'],
                    'Humedad': json_data['humedad']
                }
                connect.connectDB().insert_one(json_data)


                # Realizar operaciones con los datos recibidos
                print(json_data)

    def getTemperature(self):
        return self.temperatura

read = ESP32_reading()
try:
    while True:
        read.reading_esp32()
        pass
except KeyboardInterrupt:
    print("Interrupción del teclado detectada. El programa se ha detenido.")


