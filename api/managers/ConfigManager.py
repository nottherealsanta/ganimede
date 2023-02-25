from starlette.responses import JSONResponse
from os import getcwd
import json


class ConfigHandler:
    def __init__(self, path=f"{getcwd()}/defaults/gm.default.config.json"):
        with open(path) as f:
            self.data = json.load(f)

    async def get(self, request):
        return JSONResponse(self.data)
