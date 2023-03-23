from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.endpoints import WebSocketEndpoint
import logging
from queue import Queue
import asyncio

class WebSocketComms:
    def __init__(self):
        self.websocket = None
        self.ready = False
        self.out_queue = Queue()

    async def send(self, data: dict):
        self.out_queue.put(data)

    async def endpoint(self, websocket: WebSocket):
        
        print("endpoint")
        self.websocket = websocket
        await self.websocket.accept()

        while True:
            try:
                if self.out_queue.empty():
                    await asyncio.sleep(0.1)
                    continue
                data = self.out_queue.get()
                await self.websocket.send_json(data)
                
            except Exception as e:
                print(e)
                break
        
        await self.websocket.close()
