from starlette.routing import Route
from starlette.responses import FileResponse
from starlette.requests import Request

from os import getcwd

print(getcwd())


class RouteManager:
    def __init__(self):
        self.routes = []
        self.default_route()
        self.ui_dir = f"{getcwd()}/../ui"

    def default_route(self):
        async def index(request):
            return FileResponse(f"{self.ui_dir}/public/index.html")

        async def global_css(request: Request):
            return FileResponse(f"{self.ui_dir}/public/global.css")

        async def bundle_js(request: Request):
            return FileResponse(f"{self.ui_dir}/public/build/bundle.js")

        async def bundle_css(request: Request):
            return FileResponse(f"{self.ui_dir}/public/build/bundle.css")

        async def favicon(request: Request):
            return FileResponse(f"{self.ui_dir}/public/favicon.ico")

        self.routes.append(Route("/", index))
        self.routes.append(Route("/global.css", global_css))
        self.routes.append(Route("/build/bundle.js", bundle_js))
        self.routes.append(Route("/build/bundle.css", bundle_css))
        self.routes.append(Route("/favicon.ico", favicon))

    def add_route(self, path, func):
        self.routes.append(Route(path, func))

    def get_routes(self):
        return self.routes
