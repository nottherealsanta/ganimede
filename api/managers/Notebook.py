from os import getcwd
import json
import asyncio
import logging
from pathlib import Path

from managers.Kernel import Kernel
from managers.Comms import Comms
from managers.Cell import Cell

log = logging.getLogger(__name__)


class Notebook:
    def __init__(
        self,
        kernel: Kernel,
        comms: Comms,
        notebook_path: str = Path(f"{getcwd()}/tests/test1.ipynb"),
    ):
        self.kernel = kernel
        self.comms = comms
        self.notebook_path = notebook_path
        log.debug(notebook_path)

        self.cells = []

        self.notebook_file = self._load_notebook()

        if notebook_path is not None:
            self.init_cells()

        # websocket message queue
        self.comms_queue = comms.channel_queues["notebook"]

        asyncio.create_task(self.listen_comms())

    @property
    def id_map(self):
        return {cell.id: i for (i, cell) in enumerate(self.cells)}

    def _load_notebook(self):
        notebook_path = Path(self.notebook_path)
        if not notebook_path.exists():
            log.debug("Notebook does not exist")
            return None
        with open(notebook_path, "r") as f:
            return json.load(f)

    async def listen_comms(self):
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

        message = {
            "cells": [cell.to_dict() for cell in self.cells],
            "id_map": self.id_map,
        }
        self.comms.send(
            {
                "channel": "notebook",
                "method": "set",
                "message": message,
            }
        )

    def init_cells(self):
        for cell in self.notebook_file["cells"]:
            metadata = cell["metadata"] if "metadata" in cell else {}
            gm_metadata = metadata["gm"] if "gm" in metadata else {}

            self.cells.append(
                Cell(
                    id=None,
                    type=cell["cell_type"],
                    source=cell["source"],
                    execution_count=cell["execution_count"]
                    if "execution_count" in cell
                    else None,
                    outputs=cell["outputs"] if "outputs" in cell else [],
                    **gm_metadata,
                )
            )

        self._connect_cells()

        for cell in self.cells:
            log.debug(
                f"""cell.id {cell.id}
            cell.type {cell.type}
            cell.source \n{"".join(cell.source)}
            cell.is_heading {cell.is_heading}
            cell.heading_level {cell.heading_level}
            cell.next {cell.next}
            cell.prev {cell.prev}
            cell.parent {cell.parent}
            cell.children {cell.children}
            """
            )

    def _connect_cells(self):
        """
        forms the graph of cells
        next-prev
        parent-children
        """

        hlevel_map = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
        }
        cell_list = []
        for i, cell in enumerate(self.cells):
            if cell.is_heading:
                hlevel_map[cell.heading_level].append(i)

            cell_list.append(i)

        for level in range(6, 0, -1):
            for cell_id in hlevel_map[level]:
                index = cell_list.index(cell_id)

                i = index + 1
                children = []
                while i < len(cell_list):
                    if (
                        self.cells[i].is_heading
                        and self.cells[i].heading_level
                        == self.cells[index].heading_level
                    ):
                        self.cells[index].next = [self.cells[i].id]
                        self.cells[i].prev = [self.cells[index].id]
                        break
                    if (
                        self.cells[i].is_heading
                        and self.cells[i].heading_level
                        < self.cells[index].heading_level
                    ):
                        break

                    if len(children) > 0:
                        prev = children[-1]
                        self.cells[prev].next = [self.cells[i].id]
                        self.cells[i].prev = [self.cells[prev].id]
                    children.append(i)

                    if (
                        self.cells[i].is_heading
                        and self.cells[i].heading_level
                        > self.cells[index].heading_level
                    ):
                        last_child_id = self.cells[i].children[-1]
                        last_child_idx = self.id_map[last_child_id]

                        while len(self.cells[last_child_idx].children) > 0:
                            last_child_id = self.cells[last_child_idx].children[-1]
                            last_child_idx = self.id_map[last_child_id]

                        i = last_child_idx + 1

                        continue

                    i += 1

                self.cells[index].children = [self.cells[i].id for i in children]
                for child in children:
                    self.cells[child].parent = self.cells[index].id

                for i in range(0, len(self.cells[index].children) - 1):
                    x_id = self.cells[index].children[i]
                    y_id = self.cells[index].children[i + 1]
                    x_idx = self.id_map[x_id]
                    y_idx = self.id_map[y_id]
                    self.cells[x_idx].next = [y_id]
                    self.cells[y_idx].prev = [x_id]

        # connect the parent_less cells
        for i, cell in enumerate(self.cells):
            if cell.parent is None and not cell.is_heading:
                if i == 0:
                    continue
                prev_id = self.cells[i - 1].id
                cell.prev = [prev_id]
                self.cells[i - 1].next = [cell.id]

    # def add_metadata(self):
    #     for i in range(len(self.cells)):
    #         self.id_map[self.cells[i].id] = i

    #     if "gm" not in self.notebook["metadata"]:
    #         self.notebook["metadata"]["gm"] = {
    #             "canvas": {
    #                 "scroll": {
    #                     "x": 0,
    #                     "y": 0,
    #                 },
    #                 "zoom": 1,
    #             },
    #             "id_map": self.id_map,
    #         }

    # def save_notebook(self):
    #     log.debug("saving notebook")
    #     self.notebook["cells"] = [cell.save() for cell in self.cells]
    #     self.notebook["metadata"]["gm"]["id_map"] = self.id_map
    #     with open(self.notebook_path, "w") as f:
    #         json.dump(self.notebook, f, indent=2)

    async def run(self, cell_id: str, code: list[str]):
        msg_queue = asyncio.Queue()

        # set code to cell
        cell_index = self.id_map[cell_id]
        self.cells[cell_index].source = code
        self.cells[cell_index].outputs = []

        log.debug(f"code: {code}")

        loop = asyncio.get_event_loop()

        execute_task = loop.create_task(
            self.kernel.execute(code=code, msg_queue=msg_queue)
        )

        while True:
            msg = await msg_queue.get()

            log.debug(f"msg: {msg}")
            log.debug(f"-msg_queue size: {msg_queue.qsize()}")

            if (
                "msg_type" in msg
                and msg["msg_type"] == "status"
                and "execution_state" in msg
                and msg["execution_state"] == "idle"
            ):  # last message
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

    # async def new_code_cell(self, previous_cell_id: str):
    #     new_cell = Cell(
    #         {
    #             "cell_type": "code",
    #         }
    #     )
    #     new_cell.metadata["gm"]["previous"] = [previous_cell_id]

    #     # previous cell's
    #     previous_cell = self.cells[self.id_map[previous_cell_id]]
    #     previous_cell.metadata["gm"]["next"] = [new_cell.id]

    #     # insert new cell
    #     self.cells.insert(self.id_map[previous_cell_id] + 1, new_cell)

    #     # update id_map
    #     self.id_map[new_cell.id] = len(self.cells) - 1

    #     response = {
    #         "new_cell": new_cell.to_dict(),
    #         "previous_cell_id": previous_cell_id,
    #         "id_map": self.id_map,
    #     }

    #     log.debug(f"new cell: {new_cell.id}")

    #     self.comms.send(
    #         {
    #             "channel": "notebook",
    #             "method": "new_code_cell",
    #             "message": response,
    #         }
    #     )

    #     # TODO: refactor this
    #     self.notebook["cells"] = [cell.to_dict() for cell in self.cells]
    #     self.notebook["metadata"]["gm"]["id_map"] = self.id_map
