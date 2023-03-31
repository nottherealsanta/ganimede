import asyncio

from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.routing import Route
from starlette.responses import JSONResponse

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
    print("startup")

    route_manager = RouteManager(app)

    comms = Comms()

    config_handler = ConfigHandler()
    route_manager.add_route("/config", config_handler.get, ["GET"], "config")

    kernel = Kernel(comms)

    notebook = Notebook(kernel, comms)

    # websocket route
    route_manager.add_websocket_route("/", comms.endpoint, "ws")

    # async def send_things(request):
    #     await notebook.send_notebook()
    #     return JSONResponse({"status": "ok"})

    # route_manager.add_route("/notebook", send_things, ["GET"], "notebook")

    # print("send_notebook")
    # await notebook_manager.send_notebook()

    # get notebook route
    # route_manager.add_route(
    #     "/notebook", notebook_manager.send_notebook, ["GET"], "notebook"
    # )
    # # run cell route
    # route_manager.add_route(
    #     "/notebook/run/{cell_id}",
    #     notebook_manager.run_cell,
    #     ["POST"],
    #     "notebook_run_cell",
    # )
    # # get output route
    # route_manager.add_route(
    #     "/notebook/output/{cell_id}",
    #     notebook_manager.get_output,
    #     ["GET"],
    #     "notebook_get_output",
    # )

    # # new cell route
    # route_manager.add_route(
    #     "/notebook/new_cell", notebook_manager.new_cell, ["POST"], "notebook_new_cell", )


if __name__ == "__main__":
    print("Starting up")

    uvicorn.run(
        f"main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
