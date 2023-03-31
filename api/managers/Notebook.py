from os import getcwd, urandom
from base64 import urlsafe_b64encode
import json
import asyncio

import logging
from random import randint
from pathlib import Path
from starlette.requests import Request
from starlette.responses import JSONResponse

from managers.Kernel import Kernel
from managers.Comms import Comms

log = logging.getLogger(__name__)


class Cell:
    def __init__(self, cell_dict: dict):
        self.cell_type = cell_dict["cell_type"]

        if "source" in cell_dict:
            self.source = cell_dict["source"]
        else:
            self.source = ""

        if "execution_count" in cell_dict:
            self.execution_count = cell_dict["execution_count"]
        else:
            self.execution_count = None

        if "id" in cell_dict:
            self.id = cell_dict["id"]
        else:
            self.id = self._generate_id()

        if "outputs" in cell_dict:
            self.outputs = cell_dict["outputs"]
        if "metadata" in cell_dict:
            self.metadata = cell_dict["metadata"]
        else:
            self.metadata = {
                "gm": {
                    "top": 0,
                    "left": 0,
                    "height": 0,
                    "width": 0,
                    "previous": [],
                    "next": [],
                    "parent": None,
                    "children": [],
                }
            }
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
                "parent": None,
                "children": [],
            }

    def to_dict(self) -> dict:
        _dict = {
            "cell_type": self.cell_type,
            "metadata": self.metadata,
            "source": self.source,
            "execution_count": self.execution_count,
            "id": self.id,
        }
        if hasattr(self, "outputs"):
            _dict["outputs"] = self.outputs
        return _dict

    # def run(self, code: str, kernel=None):
    #     self.source = code

    #     self.output = kernel.execute(code)


class Notebook:
    def __init__(
        self,
        kernel: Kernel,
        comms: Comms,
        notebook_path: str = Path(f"{getcwd()}/tests/test0.ipynb"),
    ):
        self.kernel = kernel
        self.comms = comms
        self.notebook_path = notebook_path
        log.debug(notebook_path)

        # Load notebook
        def load_notebook():
            notebook_path = Path(self.notebook_path)
            if not notebook_path.exists():
                log.debug("Notebook does not exist")
                return None
            with open(notebook_path, "r") as f:
                return json.load(f)

        self.notebook = load_notebook()

        # TODO: cells must be a property that mirrors the notebook["cells"] ?
        self.cells = []
        self.init_cells()

        self.id_map = {}

        self.add_metadata()

        self.save_notebook()

        self.msg_queue: asyncio.Queue = asyncio.Queue()

        self.comms_queue = comms.channel_queues["notebook"]

        asyncio.create_task(self.listen_for_messages())

    async def listen_for_messages(self):
        while True:
            item = await self.comms_queue.get()
            method = item["method"]
            message = item["message"] if "message" in item else None

            if message:
                await getattr(self, method)(**message)
            else:
                await getattr(self, method)()

    async def get(self):
        log.debug("get notebook")
        await self.kernel.start_kernel()
        self.comms.send(
            {"channel": "notebook", "method": "set", "message": self.notebook}
        )

    def init_cells(self):
        for cell in self.notebook["cells"]:
            self.cells.append(Cell(cell))
        if (
            "gm" not in self.notebook["metadata"]
        ):  # if notebook is not already graphified
            # next and previous
            for i in range(len(self.cells)):
                current_cell = self.cells[i]
                previous_cell = self.cells[i - 1] if i > 0 else None

                if previous_cell is not None:
                    current_cell.metadata["gm"]["previous"] = [previous_cell.id]
                    previous_cell.metadata["gm"]["next"] = [current_cell.id]
            # parent and children
            for i in range(len(self.cells)):
                current_cell = self.cells[i]
                parent = None
                for j in range(i - 1, -1, -1):
                    if self.cells[j].cell_type == "markdown":
                        if any(line.startswith("#") for line in self.cells[j].source):
                            parent = self.cells[j]
                            break
                if parent is not None:
                    current_cell.metadata["gm"]["parent"] = parent.id
                    parent.metadata["gm"]["children"].append(current_cell.id)

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
        self.notebook["metadata"]["gm"]["id_map"] = self.id_map

        with open(self.notebook_path, "w") as f:
            json.dump(self.notebook, f, indent=2)

    async def run(self, cell_id: str, code: list[str]):
        self.msg_queue = asyncio.Queue()

        # set code to cell
        cell_index = self.id_map[cell_id]
        self.cells[cell_index].source = code
        self.cells[cell_index].outputs = []

        log.debug(f"code: {code}")

        loop = asyncio.get_event_loop()

        execute_task = loop.create_task(
            self.kernel.execute(code=code, msg_queue=self.msg_queue)
        )

        while True:
            msg = await self.msg_queue.get()

            log.debug(f"msg: {msg}")
            log.debug(f"-msg_queue size: {self.msg_queue.qsize()}")

            if (
                "msg_type" in msg
                and msg["msg_type"] == "status"
                and "execution_state" in msg
                and msg["execution_state"] == "idle"
            ):  # last message
                print("break")
                break

            # TODO: move this to output setter
            if "msg_type" not in msg:  # if message is an output, send it
                self.cells[cell_index].outputs.append(msg)
                message = {
                    "cell_id": cell_id,
                    "output": msg,
                }
                self.comms.send(
                    {
                        "channel": "notebook",
                        "method": "append_output",
                        "message": message,
                    }
                )

        # TODO: refactor this
        self.notebook["cells"] = [cell.to_dict() for cell in self.cells]
        self.notebook["metadata"]["gm"]["id_map"] = self.id_map

    async def new_code_cell(self, previous_cell_id: str):
        new_cell = Cell(
            {
                "cell_type": "code",
            }
        )
        new_cell.metadata["gm"]["previous"] = [previous_cell_id]

        # previous cell's
        previous_cell = self.cells[self.id_map[previous_cell_id]]
        previous_cell.metadata["gm"]["next"] = [new_cell.id]

        # insert new cell
        self.cells.insert(self.id_map[previous_cell_id] + 1, new_cell)

        # update id_map
        self.id_map[new_cell.id] = len(self.cells) - 1

        response = {
            "new_cell": new_cell.to_dict(),
            "previous_cell_id": previous_cell_id,
            "id_map": self.id_map,
        }

        log.debug(f"new cell: {new_cell.id}")

        self.comms.send(
            {
                "channel": "notebook",
                "method": "new_code_cell",
                "message": response,
            }
        )

        # TODO: refactor this
        self.notebook["cells"] = [cell.to_dict() for cell in self.cells]
        self.notebook["metadata"]["gm"]["id_map"] = self.id_map
