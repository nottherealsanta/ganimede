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
            return FileResponse(f"{self.ui_dir}/index.html")

        async def global_css(request: Request):
            return FileResponse(f"{self.ui_dir}/src/index.css")

        async def bundle_js(request: Request):
            return FileResponse(f"{self.ui_dir}/src/main.js")

        async def bundle_js_map(request: Request):
            return FileResponse(f"{self.ui_dir}/src/App.svelte")

        async def bundle_css(request: Request):
            return FileResponse(f"{self.ui_dir}/public/build/bundle.css")

        async def tailwind_app_css(request: Request):
            return FileResponse(f"{self.ui_dir}/public/css/app.css")

        async def favicon(request: Request):
            return FileResponse(f"{self.ui_dir}/public/favicon.png")

        self.app.add_route("/", index, methods=["GET"], name="index")
        self.app.add_route(
            "/src/index.css", global_css, methods=["GET"], name="global_css"
        )
        self.app.add_route(
            "/src/main.js", bundle_js, methods=["GET"], name="main_js"
        )
        self.app.add_route(
            "/src/App.svelte", bundle_js_map, methods=["GET"], name="bundle_js_map"
        )
        self.app.add_route(
            "/build/bundle.css", bundle_css, methods=["GET"], name="bundle_css"
        )
        self.app.add_route(
            "/css/app.css", tailwind_app_css, methods=["GET"], name="tailwind_app_css"
        )
        self.app.add_route("/favicon.png", favicon, methods=["GET"], name="favicon")

    def add_route(self, route_path, route_function, methods, name):
        self.app.add_route(route_path, route_function, methods=methods, name=name)

    def add_websocket_route(self, route_path, route_function, name):
        self.app.add_websocket_route(route_path, route_function, name=name)
