import logging
from os import getcwd, urandom
from base64 import urlsafe_b64encode
import json
from pathlib import Path
from starlette.requests import Request
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG)


class NotebookManager:
    def __init__(
        self,
        kernel_manager,
        notebook_path: str = Path(f"{getcwd()}/tests/test0.ipynb"),
    ):
        self.kernel_manager = kernel_manager
        self.notebook_path = notebook_path
        print(notebook_path)

        # Load notebook
        def load_notebook():
            notebook_path = Path(self.notebook_path)
            if not notebook_path.exists():
                logging.debug("Notebook does not exist")
                return None
            with open(notebook_path, "r") as f:
                return json.load(f)

        self.notebook = load_notebook()

        self.add_metadata()

        self.save_notebook()

    async def get_notebook(self, request: Request) -> JSONResponse:
        return JSONResponse(self.notebook)

    def add_metadata(self):
        def create_random_cell_id(id_length: int = 8) -> str:
            n_bytes = max(id_length * 3 // 4, 1)
            return urlsafe_b64encode(urandom(n_bytes)).decode("ascii").rstrip("=")

        self.id_map = {}
        for i in range(len(self.notebook["cells"])):
            cell = self.notebook["cells"][i]

            if "id" not in cell:
                cell["id"] = create_random_cell_id()
            self.id_map[cell["id"]] = i

        if "gm" not in self.notebook["metadata"]:
            _dict = {}
            _dict["canvas"] = {
                "scroll": {
                    "x": 0,
                    "y": 0,
                },
                "zoom": 1,
            }
            _dict["id_map"] = self.id_map
            self.notebook["metadata"]["gm"] = _dict

        # cell metadata
        for i in range(len(self.notebook["cells"])):
            current_cell = self.notebook["cells"][i]
            previous_cell = self.notebook["cells"][i - 1] if i > 0 else None

            if "gm" not in current_cell["metadata"]:
                # cell location TODO: change this
                current_cell["metadata"]["gm"] = {
                    "top": 100,
                    "left": 0,
                    "height": 0,
                    "width": 0,
                }

            if "previous" not in current_cell["metadata"]["gm"]:
                current_cell["metadata"]["gm"]["previous"] = []
            if "next" not in current_cell["metadata"]["gm"]:
                current_cell["metadata"]["gm"]["next"] = []

            if previous_cell is not None:
                current_cell["metadata"]["gm"]["previous"] = [previous_cell["id"]]
                previous_cell["metadata"]["gm"]["next"] = [current_cell["id"]]

    def save_notebook(self):
        with open(self.notebook_path, "w") as f:
            json.dump(self.notebook, f, indent=4)

    async def run_cell(self, request: Request) -> JSONResponse:
        cell_id = request.path_params["cell_id"]
        code = (await request.json())["code"]
        print(f"code: {code}")

        cell_index = self.id_map[cell_id]
        cell = self.notebook["cells"][cell_index]

        return await self.kernel_manager.execute(code)
