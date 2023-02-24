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
            return FileResponse(f"{self.ui_dir}/index.html")

        async def main_ts(request: Request):
            return FileResponse(f"{self.ui_dir}/src/main.ts")

        self.routes.append(Route("/", index))
        self.routes.append(Route("/src/main.ts", main_ts))

    def add_route(self, path, func):
        self.routes.append(Route(path, func))

    def get_routes(self):
        return self.routes
