import asyncio
import websockets
import pymongo
import json

# Configuración de la conexión a MongoDB Atlas
mongo_url = "mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/<basededatos>?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_url)
db = client["nombre_de_la_base_de_datos"]
collection = db["nombre_de_la_coleccion"]


async def handle_websocket(websocket, path):
    while True:
        # Recibir datos desde el cliente WebSocket
        data = await websocket.recv()

        # Parsear el JSON recibido
        json_data = json.loads(data)

        # Guardar los datos en la colección de MongoDB
        collection.insert_one(json_data)

        # Enviar una respuesta al cliente WebSocket
        response = "Datos guardados en MongoDB Atlas"
        await websocket.send(response)


async def start_server():
    server = await websockets.serve(handle_websocket, "0.0.0.0", 8080)
    print("Servidor WebSocket iniciado")


loop = asyncio.get_event_loop()
loop.run_until_complete(start_server())
loop.run_forever()
