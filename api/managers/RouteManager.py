from starlette.routing import Route
from starlette.responses import FileResponse
from starlette.requests import Request

from os import getcwd


class RouteManager:
    def __init__(self, app):
        self.app = app
        self.default_route()
        self.ui_dir = f"{getcwd()}/../ui"

    def default_route(self):
        async def index(request):
            return FileResponse(f"{self.ui_dir}/public/index.html")

        async def global_css(request: Request):
            return FileResponse(f"{self.ui_dir}/public/global.css")

        async def bundle_js(request: Request):
            return FileResponse(f"{self.ui_dir}/public/build/bundle.js")

        async def bundle_js_map(request: Request):
            return FileResponse(f"{self.ui_dir}/public/build/bundle.js.map")

        async def bundle_css(request: Request):
            return FileResponse(f"{self.ui_dir}/public/build/bundle.css")

        async def favicon(request: Request):
            print("favicon")
            return FileResponse(f"{self.ui_dir}/public/favicon.png")

        self.app.add_route("/", index, methods=["GET"], name="index")
        self.app.add_route(
            "/global.css", global_css, methods=["GET"], name="global_css"
        )
        self.app.add_route(
            "/build/bundle.js", bundle_js, methods=["GET"], name="bundle_js"
        )
        self.app.add_route(
            "/build/bundle.js.map", bundle_js_map, methods=["GET"], name="bundle_js_map"
        )
        self.app.add_route(
            "/build/bundle.css", bundle_css, methods=["GET"], name="bundle_css"
        )
        self.app.add_route("/favicon.png", favicon, methods=["GET"], name="favicon")

    def add_route(self, route_path, route_function, methods, name):
        self.app.add_route(route_path, route_function, methods=methods, name=name)

    def add_websocket_route(self, route_path, route_function, name):
        self.app.add_websocket_route(route_path, route_function, name=name)