#!/usr/bin/env python

import asyncio
import websockets
import pymongo
import json

# Configuración de la conexión a MongoDB Atlas
mongo_url = 'mongodb+srv://angel:angel1205@bd1.5gebju1.mongodb.net/Esp32?retryWrites=true&w=majority'
client = pymongo.MongoClient(mongo_url)
db = client["Esp32"]
collection = db["Datos"]

async def handle_client(websocket):
    while True:
        # Recibir datos desde el cliente WebSocket (ESP32)
        data = await websocket.recv()
        print(f"Datos recibidos desde el ESP32: {data}")

        try:
            # Parsear el JSON recibido
            json_data = json.loads(data)
            print(f"JSON analizado: {json_data}")

            # Guardar los datos en la colección de MongoDB
            collection.insert_one(json_data)
            print("Datos guardados en MongoDB Atlas")

            # Enviar una respuesta al ESP32
            response = "Datos recibidos y guardados correctamente"
            await websocket.send(response)
            print(f"Respuesta enviada al ESP32: {response}")
        except json.JSONDecodeError as e:
            print(f"Error al analizar JSON: {e}")



async def main():                             #Recibira de cualquier direccion
    async with websockets.serve(handle_client,"0.0.0.0", 5000):
        print('Se inicio el servidor')
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())