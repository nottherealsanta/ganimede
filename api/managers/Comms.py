from starlette.websockets import WebSocket
import logging
from asyncio import Queue
import asyncio

log = logging.getLogger(__name__)


class Comms:
    def __init__(self):
        self.websocket: WebSocket 
        self.out_queue = Queue()
        self.channel_queues = {
            "comms": Queue(),
            "notebook": Queue(),
            "kernel": Queue(),
            "config": Queue(),
        }
        self.websocket_running = asyncio.Event()

    def send(self, data: dict):
        self.out_queue.put_nowait(data)

    async def endpoint(self, websocket: WebSocket):
        log.debug("endpoint")
        self.websocket = websocket
        await self.websocket.accept()

        self.websocket_running = True

        async def send_task():
            while self.websocket_running:
                try:
                    data = await self.out_queue.get()
                    log.debug(f"send: {data}")
                    await self.websocket.send_json(data)

                except Exception as e:
                    log.debug(e)
                    break

        async def receive_task():
            while self.websocket_running:
                try:
                    data = await self.websocket.receive_json()
                    log.debug(f"received: {data}")
                    self.channel_queues[data["channel"]].put_nowait(data)

                except Exception as e:
                    self.websocket_running = False
                    log.debug(e)
                    self.out_queue.put_nowait(None)
                    break

        send = asyncio.create_task(send_task())
        receive = asyncio.create_task(receive_task())

        await asyncio.gather(send, receive)
