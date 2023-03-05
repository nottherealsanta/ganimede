import logging
from os import getcwd, urandom
from base64 import urlsafe_b64encode
import json
import asyncio
from random import randint
from pathlib import Path
from starlette.requests import Request
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG)


class Cell:
    def __init__(self, cell_dict: dict):
        self.cell_type = cell_dict["cell_type"]
        self.source = cell_dict["source"]
        self.outputs = cell_dict["outputs"]

        if "execution_count" in cell_dict:
            self.execution_count = cell_dict["execution_count"]
        else:
            self.execution_count = None

        if "id" in cell_dict:
            self.id = cell_dict["id"]
        else:
            self.id = self._generate_id()

        self.metadata = cell_dict["metadata"]
        self._add_metadata()

    def _generate_id(self, id_length: int = 8) -> str:
        n_bytes = max(id_length * 3 // 4, 1)
        return urlsafe_b64encode(urandom(n_bytes)).decode("ascii").rstrip("=")

    def _add_metadata(self):
        if "gm" not in self.metadata:
            self.metadata["gm"] = {
                "top": 0,
                "left": 0,
                "height": 0,
                "width": 0,
                "previous": [],
                "next": [],
            }

    def to_dict(self) -> dict:
        return {
            "cell_type": self.cell_type,
            "metadata": self.metadata,
            "source": self.source,
            "outputs": self.outputs,
            "execution_count": self.execution_count,
            "id": self.id,
        }

    # def run(self, code: str, kernel=None):
    #     self.source = code

    #     self.output = kernel.execute(code)


class NotebookManager:
    def __init__(
        self,
        kernel_manager,
        notebook_path: str = Path(f"{getcwd()}/tests/test0.ipynb"),
    ):
        self.kernel_manager = kernel_manager
        self.notebook_path = notebook_path
        logging.debug(notebook_path)

        # Load notebook
        def load_notebook():
            notebook_path = Path(self.notebook_path)
            if not notebook_path.exists():
                logging.debug("Notebook does not exist")
                return None
            with open(notebook_path, "r") as f:
                return json.load(f)

        self.notebook = load_notebook()

        self.cells = []
        self.init_cells()

        self.id_map = {}

        self.add_metadata()

        self.save_notebook()

        self.msg_queue: asyncio.Queue = asyncio.Queue()

    async def get_notebook(self, request: Request) -> JSONResponse:
        return JSONResponse(self.notebook)

    def init_cells(self):
        for cell in self.notebook["cells"]:
            self.cells.append(Cell(cell))
        # next and previous
        if (
            "gm" not in self.notebook["metadata"]
        ):  # if notebook is not already graphified
            for i in range(len(self.cells)):
                current_cell = self.cells[i]
                previous_cell = self.cells[i - 1] if i > 0 else None

                if previous_cell is not None:
                    current_cell.metadata["gm"]["previous"] = [previous_cell.id]
                    previous_cell.metadata["gm"]["next"] = [current_cell.id]

    def add_metadata(self):
        for i in range(len(self.cells)):
            self.id_map[self.cells[i].id] = i

        if "gm" not in self.notebook["metadata"]:
            self.notebook["metadata"]["gm"] = {
                "canvas": {
                    "scroll": {
                        "x": 0,
                        "y": 0,
                    },
                    "zoom": 1,
                },
                "id_map": self.id_map,
            }

    def save_notebook(self):
        self.notebook["cells"] = [cell.to_dict() for cell in self.cells]

        with open(self.notebook_path, "w") as f:
            json.dump(self.notebook, f, indent=2)

    async def run_cell(self, request: Request) -> JSONResponse:
        cell_id = request.path_params["cell_id"]
        code = (await request.json())["code"]
        logging.debug(f"code: {code}")

        loop = asyncio.get_event_loop()

        execute_task = loop.create_task(
            self.kernel_manager.execute(code=code, msg_queue=self.msg_queue)
        )

        return JSONResponse({"status": "ok"})

    def _parse_output(self, msg):
        output = {
            "output_type": msg["msg_type"],
        }
        if "text" in msg["content"]:
            output["text"] = [msg["content"]["text"]]
        if "name" in msg["content"]:
            output["name"] = msg["content"]["name"]
        if "execution_state" in msg["content"]:
            output["execution_state"] = msg["content"]["execution_state"]

        return output

    async def get_output(self, request: Request) -> JSONResponse:
        msg = await self.msg_queue.get()
        msg = self._parse_output(msg)
        logging.debug(f"-output_queue size: {self.msg_queue.qsize()}")
        return JSONResponse(msg)
