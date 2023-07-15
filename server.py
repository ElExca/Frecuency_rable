#!/usr/bin/env python

import asyncio
import websockets

async def handle_client(websocket):
    while True:
        message = await websocket.recv()
        print("Mensaje recibido del cliente:", message)


async def main():                             #Recibira de cualquier direccion
    async with websockets.serve(handle_client,"0.0.0.0", 5000):
        print('Se inicio el servidor')
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())