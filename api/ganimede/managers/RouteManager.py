from starlette.routing import Route
from starlette.responses import FileResponse
from starlette.requests import Request

import os
from os import getcwd


class RouteManager:
    def __init__(self, app):
        self.app = app
        self.default_route()
        self.ui_dir = f"{getcwd()}/../ui"

    def default_route(self):
        async def index(request):
            if os.environ.get("DEV") == "True":
                return FileResponse(f"{self.ui_dir}/dev/index.html")
            return FileResponse(f"{self.ui_dir}/dist/index.html")

        async def favicon(request: Request):
            path = request.path_params["path"]
            return FileResponse(f"{self.ui_dir}/dist/{path}")

        async def assets(request: Request):
            path = request.path_params["path"]
            return FileResponse(f"{self.ui_dir}/dist/assets/{path}")

        self.app.add_route("/", index, methods=["GET"], name="index")

        self.app.add_route("/favicon.ico", favicon, methods=["GET"])

        self.app.add_route("/assets/{path:path}", assets, methods=["GET"])

    def add_route(self, route_path, route_function, methods, name):
        self.app.add_route(route_path, route_function, methods=methods, name=name)

    def add_websocket_route(self, route_path, route_function, name):
        self.app.add_websocket_route(route_path, route_function, name=name)
