import asyncio
import websockets
# import pymysql

endpoint = "protocredits"

async def on_message(websocket:websockets.WebSocketClientProtocol, message:str):
    await websocket.send("Hi")