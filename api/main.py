import asyncio

from starlette.applications import Starlette

import uvicorn

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


if __name__ == "__main__":
    print("Starting up")

    uvicorn.run(
        f"main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
