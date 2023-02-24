import asyncio

from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.routing import Route
import uvicorn

from RouteManager import RouteManager

# from NotebookHandler import NotebookHandler
# from ConfigHandler import ConfigHandler
# from KernelManager import KernelManager

loop = asyncio.get_event_loop()
app = Starlette(debug=True)


# # TODO: https://www.starlette.io/endpoints/#:~:text=class%20Echo(WebSocketEndpoint)%3A%0A%20%20%20%20encoding%20%3D%20%22text%22%0A%0A%20%20%20%20async%20def%20on_receive(self%2C%20websocket%2C%20data)%3A%0A%20%20%20%20%20%20%20%20await%20websocket.send_text(f%22Message%20text%20was%3A%20%7Bdata%7D%22)
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         mesg = await websocket.receive_text()
#         print(mesg)
#         await websocket.send_text(mesg.replace("Client", "Server"))
#     await websocket.close()


@app.on_event("startup")
async def on_startup():
    route_manager = RouteManager()
    # config_handler = ConfigHandler()
    # kernel_manager = KernelManager()
    # notebook_handler = NotebookHandler(kernel_manager)

    # route_manager.add_route("/notebook", notebook_handler.get)
    # route_manager.add_route("/notebook/run", notebook_handler.run_cell, methods=["POST"])
    # route_manager.add_route("/config", config_handler.get)

    # TODO: add this to the route manager
    routes_list = route_manager.get_routes()
    for route in routes_list:
        app.add_route(
            route.path, route.endpoint, methods=route.methods, name=route.name
        )
    # app.add_route(
    #     path="/notebook", route=notebook_handler.get, methods=["GET"], name="notebook"
    # )
    # app.add_route(
    #     path="/notebook/run",
    #     route=notebook_handler.run_cell,
    #     methods=["POST"],
    #     name="notebook_run",
    # )
    # app.add_route(
    # path="/config", route=config_handler.get, methods=["GET"], name="config"
    # )
    # app.add_websocket_route("/ws", websocket_endpoint)

    print("startup complete")


if __name__ == "__main__":
    print("Starting up")

    uvicorn.run(f"main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
