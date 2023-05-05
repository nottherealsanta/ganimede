from os import getcwd
import json
import asyncio
import queue
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
        notebook_path: str = Path(f"{getcwd()}/tests/test2.ipynb"),
    ):
        self.kernel = kernel
        self.comms = comms
        self.notebook_path = notebook_path
        log.debug(notebook_path)

        self.cells = []
        self.np_graph = {}  # next-prev directed graph
        self.pc_graph = {}  # parent-children directed graph

        self.notebook_file = self._load_notebook()

        if notebook_path is not None:
            self.init_cells()

        # websocket message queue
        self.comms_queue = comms.channel_queues["notebook"]
        asyncio.create_task(self.listen_comms())

        self.run_queue = asyncio.Queue()
        asyncio.create_task(self.run_queue_loop())

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
            "np_graph": self.np_graph,
            "pc_graph": self.pc_graph,
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
            """
            )
        log.debug(f"np_graph {self.np_graph}")
        log.debug(f"pc_graph {self.pc_graph}")

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
                self.pc_graph[cell.id] = []

            cell_list.append(i)

        for level in range(6, 0, -1):
            for cell_id in hlevel_map[level]:
                index = cell_list.index(cell_id)
                log.debug(f"cell_id {cell_id} index {index}")

                i = index + 1
                children = []
                while i < len(cell_list):
                    if (
                        self.cells[i].is_heading
                        and self.cells[i].heading_level
                        == self.cells[index].heading_level
                    ):
                        self.np_graph[self.cells[index].id] = [self.cells[i].id]
                        break
                    if (
                        self.cells[i].is_heading
                        and self.cells[i].heading_level
                        < self.cells[index].heading_level
                    ):
                        break

                    if len(children) > 0:
                        prev = children[-1]
                        self.np_graph[self.cells[prev].id] = [self.cells[i].id]
                    children.append(i)

                    if (
                        self.cells[i].is_heading
                        and self.cells[i].heading_level
                        > self.cells[index].heading_level
                    ):
                        last_child_id = self.pc_graph[self.cells[i].id][-1]
                        last_child_idx = self.id_map[last_child_id]

                        while (
                            self.cells[last_child_idx].id in self.pc_graph
                            and len(self.pc_graph[self.cells[last_child_idx].id]) > 0
                        ):
                            last_child_id = self.pc_graph[
                                self.cells[last_child_idx].id
                            ][-1]
                            last_child_idx = self.id_map[last_child_id]

                        i = last_child_idx + 1

                        continue

                    i += 1

                for child in children:
                    if self.cells[index].id not in self.pc_graph:
                        self.pc_graph[self.cells[index].id] = []
                    self.pc_graph[self.cells[index].id].append(self.cells[child].id)

                log.debug(self.pc_graph)
                for i in range(0, len(self.pc_graph[self.cells[index].id]) - 1):
                    x_id = self.pc_graph[self.cells[index].id][i]
                    y_id = self.pc_graph[self.cells[index].id][i + 1]
                    x_idx = self.id_map[x_id]
                    y_idx = self.id_map[y_id]
                    self.np_graph[x_id] = [y_id]

        # connect the parent_less cells
        parent_less_cells = []
        for i, cell in enumerate(self.cells):
            if cell.id not in self.pc_graph:
                for cell_id in self.pc_graph.keys():
                    if cell.id in self.pc_graph[cell_id]:
                        break
                else:
                    parent_less_cells.append(cell.id)
        for i, cell in enumerate(parent_less_cells):
            idx = self.id_map[cell]
            if idx < len(self.cells) - 1:
                self.np_graph[cell] = [self.cells[idx + 1].id]

    async def queue_cell(self, cell_id: str, code: list[str]):
        log.debug(f"queue_cell: {cell_id}")
        self.run_queue.put_nowait((cell_id, code))
        self._change_cell_state(cell_id, "queued")

    async def interrupt_kernel(self):
        await self.empty_run_queue()
        await self.kernel.interrupt()

    async def run_queue_loop(self):
        while True:
            cell_id, code = await self.run_queue.get()
            self._change_cell_state(cell_id, "running")
            self._clear_outputs(cell_id)
            await self.run(cell_id, code)

    async def empty_run_queue(self):
        log.debug("empty_run_queue")
        while self.run_queue.qsize() > 0:
            cell_id, _ = self.run_queue.get_nowait()
            self._change_cell_state(cell_id, "idle")

    def _clear_outputs(self, cell_id: str):
        self.cells[self.id_map[cell_id]].outputs = []
        self.comms.send(
            {
                "channel": "notebook",
                "method": "clear_outputs",
                "message": {
                    "cell_id": cell_id,
                },
            }
        )

    def _change_cell_state(self, cell_id: str, state: str):
        self.cells[self.id_map[cell_id]].state = state
        self.comms.send(
            {
                "channel": "notebook",
                "method": "change_cell_state",
                "message": {
                    "cell_id": cell_id,
                    "state": state,
                },
            }
        )

    def _set_execution_count(self, cell_id: str, execution_count: int):
        self.cells[self.id_map[cell_id]].execution_count = execution_count
        self.comms.send(
            {
                "channel": "notebook",
                "method": "set_execution_count",
                "message": {
                    "cell_id": cell_id,
                    "execution_count": execution_count,
                },
            }
        )

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

        execution_count_already_set = False
        is_kernel_idle = False

        while True:
            msg = await msg_queue.get()

            log.debug(f"msg: {msg}")
            log.debug(f"-msg_queue size: {msg_queue.qsize()}")

            if "msg_type" in msg and msg["msg_type"] == "execute_reply":
                self._set_execution_count(cell_id, msg["execution_count"])
                execution_count_already_set = True

            if (
                "msg_type" in msg
                and msg["msg_type"] == "status"
                and "execution_state" in msg
                and msg["execution_state"] == "idle"
            ):  # last message
                self._change_cell_state(cell_id, "idle")
                is_kernel_idle = True

            if execution_count_already_set and is_kernel_idle:  # last message
                break

            # TODO: move this to output setter
            if "msg_type" not in msg:  # if message is an output, send it
                # if the message is an error, clear the run queue
                if msg["output_type"] == "error":
                    await self.empty_run_queue()

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

    def _find_parent(self, cell_id: str):
        for key in self.pc_graph.keys():
            if cell_id in self.pc_graph[key]:
                return key
        return None

    async def new_code_cell(self, previous_cell_id: str):
        log.debug(f"previous cell: {previous_cell_id}")
        log.debug(f"cells: {self.cells}")

        new_cell = Cell(
            type="code",
            source=[" "],
        )

        #         new_cell["top"] = previous_cell["top"] + previous_cell["height"] + 5;
        # new_cell["left"] = previous_cell["left"];

        prev_cell = self.cells[self.id_map[previous_cell_id]]
        new_cell.top = prev_cell.top + prev_cell.height + 5
        new_cell.left = prev_cell.left

        print(prev_cell.to_dict())
        print(prev_cell.top)

        # self.cells.insert(self.id_map[previous_cell_id] + 1, new_cell)
        self.cells.append(new_cell)

        if previous_cell_id not in self.np_graph:
            self.np_graph[previous_cell_id] = [new_cell.id]
        else:
            self.np_graph[previous_cell_id].append(new_cell.id)

        prev_parent = self._find_parent(previous_cell_id)
        if prev_parent is not None:
            if prev_parent not in self.pc_graph:
                self.pc_graph[prev_parent] = [new_cell.id]
            else:
                self.pc_graph[prev_parent].append(new_cell.id)

        response = {
            "new_cell": new_cell.to_dict(),
            "previous_cell_id": previous_cell_id,
            "id_map": self.id_map,
            "np_graph": self.np_graph,
            "pc_graph": self.pc_graph,
        }

        log.debug(f"new cell: {new_cell.id}")

        self.comms.send(
            {
                "channel": "notebook",
                "method": "new_code_cell",
                "message": response,
            }
        )

        self.comms.send(
            {
                "channel": "notebook",
                "method": "resize_ancestors",
                "message": {
                    "cell_id": previous_cell_id,
                },
            }
        )

    async def new_markdown_cell(self, previous_cell_id: str):
        log.debug(f"previous cell: {previous_cell_id}")
        log.debug(f"cells: {self.cells}")

        new_cell = Cell(
            type="markdown",
            source=[""],
        )

        self.cells.insert(self.id_map[previous_cell_id] + 1, new_cell)

        if previous_cell_id not in self.np_graph:
            self.np_graph[previous_cell_id] = [new_cell.id]
        else:
            self.np_graph[previous_cell_id].append(new_cell.id)

        prev_parent = self._find_parent(previous_cell_id)
        if prev_parent is not None:
            if prev_parent not in self.pc_graph:
                self.pc_graph[prev_parent] = [new_cell.id]
            else:
                self.pc_graph[prev_parent].append(new_cell.id)

        response = {
            "new_cell": new_cell.to_dict(),
            "previous_cell_id": previous_cell_id,
            "id_map": self.id_map,
            "np_graph": self.np_graph,
            "pc_graph": self.pc_graph,
        }

        log.debug(f"new cell: {new_cell.id}")

        self.comms.send(
            {
                "channel": "notebook",
                "method": "new_markdown_cell",
                "message": response,
            }
        )

        self.comms.send(
            {
                "channel": "notebook",
                "method": "resize_ancestors",
                "message": {
                    "cell_id": previous_cell_id,
                },
            }
        )

    async def sync_cell_properties(self, cell_id: str, sync: dict):
        cell = self.cells[self.id_map[cell_id]]
        for key in sync.keys():
            setattr(cell, key, sync[key])
