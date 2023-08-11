from starlette.routing import Route
from starlette.responses import FileResponse
from starlette.requests import Request

import os
from os import getcwd
import importlib.resources

files = importlib.resources.files('ui_dist')

class RouteManager:
    def __init__(self, app):
        self.app = app
        self.default_route()
        self.ui_dir = f"{getcwd()}/../ui"

    def default_route(self):
        async def index(request):
            if os.environ.get("DEV") == "True":
                return FileResponse(f"{self.ui_dir}/dev/index.html")

            file_path = files.joinpath("../ui_dist/index.html")
            return FileResponse(file_path)
            # return FileResponse(f"{self.ui_dir}/dist/index.html")

        async def favicon(request: Request):
            path = request.path_params["path"]
            # return FileResponse(f"{self.ui_dir}/dist/{path}")
            file_path = files.joinpath(f"../ui_dist/{path}")
            return FileResponse(file_path)

        async def codicon(request: Request):
            # return FileResponse(f"{self.ui_dir}/dist/codicon.ttf")
            file_path = files.joinpath("../ui_dist/codicon.ttf")
            return FileResponse(file_path)
        
        async def assets(request: Request):
            path = request.path_params["path"]
            # return FileResponse(f"{self.ui_dir}/dist/assets/{path}")
            file_path = files.joinpath(f"../ui_dist/assets/{path}")
            return FileResponse(file_path)

        self.app.add_route("/", index, methods=["GET"], name="index")

        self.app.add_route("/favicon.ico", favicon, methods=["GET"])
        
        self.app.add_route("/codicon.ttf", codicon, methods=["GET"])
        self.app.add_route("/node_modules/monaco-editor/esm/vs/base/browser/ui/codicons/codicon/codicon.ttf", codicon, methods=["GET"])

        self.app.add_route("/assets/{path:path}", assets, methods=["GET"])

    def add_route(self, route_path, route_function, methods, name):
        self.app.add_route(route_path, route_function, methods=methods, name=name)

    def add_websocket_route(self, route_path, route_function, name):
        self.app.add_websocket_route(route_path, route_function, name=name)
