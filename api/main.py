import asyncio

from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.routing import Route
import uvicorn

from managers.RouteManager import RouteManager
from managers.ConfigManager import ConfigHandler
from managers.KernelManager import KernelManger
from managers.NotebookManager import NotebookManager

loop = asyncio.get_event_loop()
app = Starlette(debug=True)


@app.on_event("startup")
async def on_startup():
    route_manager = RouteManager(app)

    config_handler = ConfigHandler()
    route_manager.add_route("/config", config_handler.get, ["GET"], "config")

    kernel_manager = KernelManger()

    notebook_manager = NotebookManager(kernel_manager)
    route_manager.add_route(
        "/notebook", notebook_manager.get_notebook, ["GET"], "notebook"
    )
    # route for running with cell id
    route_manager.add_route(
        "/notebook/run/{cell_id}",
        notebook_manager.run_cell,
        ["POST"],
        "notebook_run_cell",
    )
    # route for retriving output with cell id
    route_manager.add_route(
        "/notebook/output/{cell_id}",
        notebook_manager.get_output,
        ["GET"],
        "notebook_get_output",
    )

    # new cell route
    route_manager.add_route(
        "/notebook/new_cell", notebook_manager.new_cell, ["POST"], "notebook_new_cell", )


if __name__ == "__main__":
    print("Starting up")

    uvicorn.run(
        f"main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
