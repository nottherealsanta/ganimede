import asyncio

from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.routing import Route
import uvicorn

from RouteManager import RouteManager

loop = asyncio.get_event_loop()
app = Starlette(debug=True)


@app.on_event("startup")
async def on_startup():
    route_manager = RouteManager()

    routes_list = route_manager.get_routes()
    for route in routes_list:
        app.add_route(
            route.path, route.endpoint, methods=route.methods, name=route.name
        )

    print("startup complete")


if __name__ == "__main__":
    print("Starting up")

    uvicorn.run(f"main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
