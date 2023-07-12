import asyncio

from starlette.applications import Starlette
from starlette.background import BackgroundTask
import y_py as Y
from ypy_websocket import ASGIServer, WebsocketServer, WebsocketProvider
import uvicorn
from websockets import serve, connect


from managers.RouteManager import RouteManager
from managers.ConfigManager import ConfigHandler
from managers.Kernel import Kernel
from managers.Comms import Comms
from managers.Notebook import Notebook

import logging
import sys

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger(__name__)

loop = asyncio.get_event_loop()
app = Starlette(debug=True)

websocket_server = WebsocketServer()
yapp = ASGIServer(websocket_server)

@app.on_event("startup")
async def on_startup():
    log.info("Starting up")

    route_manager = RouteManager(app)

    comms = Comms()

    config_handler = ConfigHandler()
    route_manager.add_route("/config", config_handler.get, ["GET"], "config")

    kernel = Kernel(comms)

    notebook = Notebook(kernel, comms)

    # websocket route
    route_manager.add_websocket_route("/", comms.endpoint, "ws")

    # yapp server
    loop.create_task(server_task())

    # yapp client
    loop.create_task(client_task())



async def server_task():
    async with (
        WebsocketServer() as websocket_server,
        serve(websocket_server.serve, "localhost", 1234),
    ):
        await asyncio.Future()  # run forever

async def client_task():
    ydoc = Y.YDoc()
    # wait for 3 seconds
    await asyncio.sleep(0.5)
    async with (
        connect("ws://localhost:1234/g-y-room") as websocket,
        WebsocketProvider(ydoc, websocket),
    ):
        # Changes to remote ydoc are applied to local ydoc.
        # Changes to local ydoc are sent over the WebSocket and
        # broadcast to all clients.
        ymap = ydoc.get_map("map")
        with ydoc.begin_transaction() as t:
            ymap.set(t, "testing_key", "testing_value")

        await asyncio.Future()  # run forever


if __name__ == "__main__":
    log.info("Starting up")

    uvicorn.run(
        f"main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
   


