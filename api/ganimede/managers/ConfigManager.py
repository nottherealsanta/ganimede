from starlette.responses import JSONResponse
from os import getcwd


class ConfigHandler:
    def __init__(self):
        self.data = {
            "monaco": {
                "fontSize": 13,
                "lineNumbers": "on"
            },
            "outputs": {
                "fontSize": 14
            },
            "grid": {
                "snap": {
                    "x": 20,
                    "y": 20
                }
            }
        }

    async def get(self, request):
        return JSONResponse(self.data)
