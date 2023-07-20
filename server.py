import asyncio
import websockets
import pymongo
import json

# Configuración de la conexión a MongoDB Atlas
mongo_url = 'url'
client = pymongo.MongoClient(mongo_url)
db = client["Esp32"]
collection = db["Datos"]

clientes = {}

async def handle_client(websocket, path):
    # Obtener el identificador del cliente
    client_id = id(websocket)

    # Agregar la conexión del cliente al diccionario
    clientes[client_id] = websocket

    try:
        while True:
            # Recibir datos desde el cliente WebSocket (ESP32)
            data = await websocket.recv()
            print(f"Datos recibidos desde el ESP32: {data}")

            try:
                # Parsear el JSON recibido
                json_data = json.loads(data)
                print(f"JSON analizado: {json_data}")

                # Convertir los valores a números y redondearlos a dos decimales
                json_data["Humidity"] = round(float(json_data["Humidity"]), 2)
                json_data["Temperature"] = round(float(json_data["Temperature"]), 2)
                json_data["CO2"] = round(float(json_data["CO2"]), 2)
                json_data["Pressure"] = round(float(json_data["Pressure"]), 2)
                json_data["Altitude"] = round(float(json_data["Altitude"]), 2)

                # Guardar los datos en la colección de MongoDB
                collection.insert_one(json_data)
                print("Datos guardados en MongoDB Atlas")
                del json_data["_id"]

                # Enviar los datos json_data al cliente WebSocket en formato JSON
                json_data_str = json.dumps(json_data)

                # Enviar el JSON a todos los clientes conectados
                for cliente_id, cliente in clientes.items():
                    await cliente.send(json_data_str)

                print("Clientes conectados:")
                for cliente_id in clientes:
                    print(cliente_id)

            except websockets.exceptions.ConnectionClosedOK:
                # No imprimir nada en esta excepción ya que es una desconexión normal
                pass
            except Exception as e:
                print(f"Ocurrió un error: {e}")
    finally:
        # Al salir del bucle, eliminar la conexión del cliente del diccionario
        del clientes[client_id]

async def main():
    # Recibirá de cualquier dirección
    async with websockets.serve(handle_client, "0.0.0.0", 5000):
        print('Se inició el servidor')
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
