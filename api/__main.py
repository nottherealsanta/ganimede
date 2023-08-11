import asyncio

from starlette.applications import Starlette
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
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger(__name__)
log.propagate = False

loop = asyncio.get_event_loop()
app = Starlette(debug=True)

websocket_server = WebsocketServer()
yapp = ASGIServer(websocket_server)
ydoc = Y.YDoc()

@app.on_event("startup")
async def on_startup():
    log.info("Starting up")

    route_manager = RouteManager(app)

    comms = Comms()
    
    # yapp server
    loop.create_task(server_task())
    # yapp client
    await asyncio.sleep(0.5) # wait for server to start
    websocket = await connect("ws://localhost:1234/g-y-room")
    websocket_provider = WebsocketProvider(ydoc, websocket, log=log)
    task = asyncio.create_task(websocket_provider.start())
    await websocket_provider.started.wait()

    config_handler = ConfigHandler()
    route_manager.add_route("/config", config_handler.get, ["GET"], "config")

    kernel = Kernel(comms, ydoc)

    notebook = Notebook(kernel, comms, ydoc)

    # websocket route
    route_manager.add_websocket_route("/", comms.endpoint, "ws")

async def server_task():
    async with (
        WebsocketServer(log=log) as websocket_server,
        serve(websocket_server.serve, "localhost", 1234, close_timeout=1),
    ):
        await asyncio.Future()  # run forever

@app.on_event("shutdown")
async def on_shutdown():
    log.info("Shutting down")


if __name__ == "__main__":
    log.info("Starting up")

    uvicorn.run(
        f"main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
   


