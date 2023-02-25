import asyncio

from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.routing import Route
import uvicorn

from managers.RouteManager import RouteManager
from managers.ConfigManager import ConfigHandler

loop = asyncio.get_event_loop()
app = Starlette(debug=True)


@app.on_event("startup")
async def on_startup():
    route_manager = RouteManager(app)

    config_handler = ConfigHandler()
    route_manager.add_route("/config", config_handler.get, ["GET"], "config")


if __name__ == "__main__":
    print("Starting up")

    uvicorn.run(
        f"main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
