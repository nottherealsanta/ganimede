import os
import click
import asyncio
import logging
import uvicorn
import y_py as Y
from rich.logging import RichHandler
from websockets import serve, connect
from starlette.applications import Starlette
from ypy_websocket import ASGIServer, WebsocketServer, WebsocketProvider

# managers
from .managers.RouteManager import RouteManager
from .managers.ConfigManager import ConfigHandler
from .managers.Kernel import Kernel
from .managers.Comms import Comms
from .managers.Notebook import Notebook

# logging
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger(__name__)
log.propagate = False

# app
# loop = asyncio.get_event_loop()
app = Starlette(debug=True)

# yapp server
websocket_server = WebsocketServer()
yapp = ASGIServer(websocket_server)
ydoc = Y.YDoc()

# yapp server task
async def server_task():
    async with (
        WebsocketServer(log=log) as websocket_server,
        serve(websocket_server.serve, "localhost", 1234, close_timeout=1),
    ):
        await asyncio.Future()  # run forever

# on startup
@app.on_event("startup")    
async def on_startup():
    route_manager = RouteManager(app)
    comms = Comms()

    loop = asyncio.get_event_loop()
    # yapp server
    _task = loop.create_task(server_task())

    # yapp client
    await asyncio.sleep(0.5) # wait for server to start
    websocket = await connect("ws://localhost:1234/g-y-room")
    websocket_provider = WebsocketProvider(ydoc, websocket, log=log)
    task = asyncio.create_task(websocket_provider.start())
    await websocket_provider.started.wait()


    config_handler = ConfigHandler()
    route_manager.add_route("/config", config_handler.get, ["GET"], "config")

    kernel = Kernel(comms, ydoc)

    notebook = Notebook(notebook_path=os.environ["NOTEBOOK_LOC"], kernel=kernel, comms=comms, ydoc=ydoc)

    # websocket route
    route_manager.add_websocket_route("/", comms.endpoint, "ws")


# cli
@click.command()
@click.argument("file")
def cli(file):

    log.info("Starting up")
    notebook_loc = os.path.abspath(file)

    os.environ["NOTEBOOK_LOC"] = notebook_loc

    uvicorn.run(
        app=f"ganimede.main:app",  
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False,
    )

# dev cli
@click.command()
@click.argument("file")
def dev_cli(file):

    log.info("Starting up")
    notebook_loc = os.path.abspath(file)

    os.environ["NOTEBOOK_LOC"] = notebook_loc
    os.environ["DEV"] = "True"

    uvicorn.run(
        app=f"ganimede.main:app",  
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )


if __name__ == "__main__":
    cli()