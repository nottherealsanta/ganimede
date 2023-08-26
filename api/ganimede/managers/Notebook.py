from os import getcwd
import json
import asyncio
import queue
import logging
from pathlib import Path
import y_py as Y
from os import urandom
from base64 import urlsafe_b64encode

from .Kernel import Kernel
from .Comms import Comms

log = logging.getLogger(__name__)


class Notebook:
    def __init__(
        self,
        kernel: Kernel,
        comms: Comms,
        ydoc: Y.YDoc,
        notebook_path: str,
    ):
        self.kernel = kernel
        self.comms = comms
        self.ydoc = ydoc
        self.notebook_path = notebook_path
        log.debug(notebook_path)

        self.np_graph = {}  # next-prev directed graph'
        self.pc_graph = {}  # parent-children directed graph

        self.notebook_file = self._load_notebook()

        with self.ydoc.begin_transaction() as t:
            self.ydoc.get_text("nb_path").insert(t, 0, self.notebook_path)

        # websocket message queue
        self.comms_queue = comms.channel_queues["notebook"]
        asyncio.create_task(self.listen_comms())

        self.run_queue = asyncio.Queue()
        asyncio.create_task(self.run_queue_loop())
        self.yrun_queue = self.ydoc.get_array("run_queue")
        # self.ydoc.get_array("run_queue").observe(self.yrun_queue_event)

        if notebook_path is not None:
            self.init_cells()

    def _load_notebook(self):
        notebook_path = Path(self.notebook_path)
        if not notebook_path.exists():
            log.info("Notebook does not exist")
            raise FileNotFoundError
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
        log.info("GET notebook")

    def init_cells(self):
        ## y
        self.ycells = self.ydoc.get_array("cells")
        ### set from file
        for cell in self.notebook_file["cells"]:
            gm_metadata = cell["metadata"]["gm"] if "gm" in cell["metadata"] else {}
            id = cell["id"] if "id" in cell else _generate_random_cell_id()
            source = Y.YText(("".join(cell["source"])))
            outputs = Y.YArray(cell["outputs"] if "outputs" in cell else [])

            ycell = self.ydoc.get_map(id)
            with self.ydoc.begin_transaction() as t:
                ycell.set(t, "id", id)
                ycell.set(t, "type", cell["cell_type"])  # code, markdown
                ycell.set(t, "source", source)
                ycell.set(
                    t,
                    "execution_count",
                    cell["execution_count"] if "execution_count" in cell else None,
                )
                ycell.set(t, "outputs", outputs)
                # gm
                ycell.set(
                    t, "top", gm_metadata["top"] if "top" in gm_metadata else None
                )
                ycell.set(
                    t, "left", gm_metadata["left"] if "left" in gm_metadata else None
                )
                ycell.set(
                    t,
                    "height",
                    gm_metadata["height"] if "height" in gm_metadata else None,
                )
                ycell.set(
                    t, "width", gm_metadata["width"] if "width" in gm_metadata else None
                )
                ycell.set(
                    t,
                    "collapsed",
                    gm_metadata["collapsed"] if "collapsed" in gm_metadata else None,
                )  # i, o, b, h
                ycell.set(t, "state", "idle")  # idle, running, queued, done

                # ycells
                self.ycells.append(t, id)

        # np_graph and pc_graph
        notebook_metadata = self.notebook_file["metadata"]
        if "gm" not in notebook_metadata:
            self._connect_cells()
        else:
            self.np_graph = notebook_metadata["gm"]["np_graph"]
            self.pc_graph = notebook_metadata["gm"]["pc_graph"]

        # y
        self.ynp_graph = self.ydoc.get_map("np_graph")
        self.ypc_graph = self.ydoc.get_map("pc_graph")
        ### set from file
        with self.ydoc.begin_transaction() as t:
            for id in self.np_graph.keys():
                nexts = Y.YArray(self.np_graph[id])
                self.ynp_graph.set(t, id, nexts)
            for id in self.pc_graph.keys():
                children = Y.YArray(self.pc_graph[id])
                self.ypc_graph.set(t, id, children)

        log.info(f"np_graph:{self.np_graph}")
        log.info(f"pc_graph:{self.pc_graph}")
        log.info(f"ynp_graph:{self.ynp_graph}")
        log.info(f"ypc_graph:{self.ypc_graph}")

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
        cells = []
        for i, cell_id in enumerate(self.ycells):
            cell = self.ydoc.get_map(cell_id)
            source = cell.get("source").__str__()
            id = cell.get("id").__str__()
            if source.startswith("#") and cell.get("type") == "markdown":
                hlevel_map[source.split("/n")[0].count("#")].append(
                    i
                )  # TODO: this should be first n consecutive chars
                self.pc_graph[id] = []
            cells.append(
                {
                    "id": id,
                    "is_heading": source.startswith("#")
                    and cell.get("type") == "markdown",
                    "heading_level": source.split("/n")[0].count("#")
                    if source.startswith("#") and cell.get("type") == "markdown"
                    else None,
                }
            )
            cell_list.append(i)

        log.info(f"hlevel_map: {hlevel_map}")
        log.info(f"cell_list: {cell_list}")

        for level in range(6, 0, -1):
            for cell_id in hlevel_map[level]:
                index = cell_list.index(cell_id)
                log.debug(f"cell_id {cell_id} index {index}")

                i = index + 1
                children = []
                while i < len(cell_list):
                    if (
                        cells[i]["is_heading"]
                        and cells[i]["heading_level"] <= cells[index]["heading_level"]
                    ):
                        break

                    children.append(i)

                    if (
                        cells[i]["is_heading"]
                        and cells[i]["heading_level"] > cells[index]["heading_level"]
                        and len(self.pc_graph[cells[i]["id"]]) > 0
                    ):
                        last_child_id = self.pc_graph[cells[i]["id"]][-1]
                        last_child_idx = [
                            i
                            for i, cell in enumerate(cells)
                            if cell["id"] == last_child_id
                        ][0]

                        # while last_child is a heading and has children
                        # last_child = that heading's last child
                        while (
                            cells[last_child_idx]["is_heading"]
                            and len(self.pc_graph[cells[last_child_idx]["id"]]) > 0
                        ):
                            last_child_id = self.pc_graph[cells[last_child_idx]["id"]][
                                -1
                            ]
                            last_child_idx = [
                                i
                                for i, cell in enumerate(cells)
                                if cell["id"] == last_child_id
                            ][0]

                        i = last_child_idx + 1

                        continue

                    i += 1
                for child in children:
                    if cells[index]["id"] not in self.pc_graph:
                        self.pc_graph[cells[index]["id"]] = []
                    self.pc_graph[cells[index]["id"]].append(cells[child]["id"])

        # connect the parent_less cells
        parent_less_cells = []
        for i, cell in enumerate(cells):
            if cell["heading_level"] == 1:
                parent_less_cells.append(cell["id"])
            elif cell["id"] not in self.pc_graph:
                for x in self.pc_graph.keys():
                    if cell["id"] in self.pc_graph[x]:
                        break
                else:
                    parent_less_cells.append(cell["id"])

        log.info(f"parent_less_cells: {parent_less_cells}")
        for i, cell_id in enumerate(parent_less_cells):
            if i < len(parent_less_cells) - 1:
                self.np_graph[cell_id] = [parent_less_cells[i + 1]]

                # debug
        for cell in cells:
            log.info(cell)

    async def queue_cell(self, cell_id: str):
        log.debug(f"queue_cell: {cell_id}")
        self.run_queue.put_nowait((cell_id))
        self._change_cell_state(cell_id, "queued")
        with self.ydoc.begin_transaction() as t:
            self.ydoc.get_array("run_queue").append(t, cell_id)

    async def interrupt_kernel(self):
        await self.empty_run_queue()
        await self.kernel.interrupt()

    # def yrun_queue_event(self, event):
    #     print(event.delta)
    #     print(type(event.delta))

    #     for i in event.insert:
    #         self.run_queue.put_nowait(i)

    async def run_queue_loop(self):
        while True:
            cell_id = await self.run_queue.get()
            self._change_cell_state(cell_id, "running")
            self._clear_outputs(cell_id)
            await self.run(cell_id)
            with self.ydoc.begin_transaction() as t:
                self.ydoc.get_array("run_queue").delete(t, 0)

    async def empty_run_queue(self):
        log.debug("empty_run_queue")
        while self.run_queue.qsize() > 0:
            cell_id = self.run_queue.get_nowait()
            self._change_cell_state(cell_id, "idle")
            with self.ydoc.begin_transaction() as t:
                self.ydoc.get_array("run_queue").delete_range(
                    t, 0, len(self.ydoc.get_array("run_queue"))
                )

    def _clear_outputs(self, cell_id: str):
        with self.ydoc.begin_transaction() as t:
            self.ydoc.get_map(cell_id).set(t, "outputs", Y.YArray([]))

    def _change_cell_state(self, cell_id: str, state: str):
        with self.ydoc.begin_transaction() as t:
            self.ydoc.get_map(cell_id).set(t, "state", state)

    def _set_execution_count(self, cell_id: str, execution_count: int):
        with self.ydoc.begin_transaction() as t:
            self.ydoc.get_map(cell_id).set(t, "execution_count", execution_count)

    async def run(self, cell_id: str):
        msg_queue = asyncio.Queue()

        loop = asyncio.get_event_loop()

        code = self.ydoc.get_map(cell_id).get("source").__str__()
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
                is_kernel_idle = True

            if execution_count_already_set and is_kernel_idle:  # last message
                break

            # TODO: move this to output setter
            if "msg_type" not in msg:  # if message is an output, send it
                # if the message is an error, clear the run queue
                if msg["output_type"] == "error":
                    await self.empty_run_queue()

                with self.ydoc.begin_transaction() as t:
                    self.ydoc.get_map(cell_id).get("outputs").append(t, msg)

        self._change_cell_state(cell_id, "idle")

    def _find_parent(self, cell_id: str):
        for key in self.pc_graph.keys():
            if cell_id in self.pc_graph[key]:
                return key
        return None

    def init_tlhw(self):
        self.comms.send(
            {
                "channel": "notebook",
                "method": "init_tlhw",
            }
        )

    async def checkpoint(self):
        notebook = {
            "cells": [],
            "metadata": {
                "gm": {
                    "np_graph": {},
                    "pc_graph": {},
                }
            },
        }

        # Collect cells
        for cell_id in self.ycells:
            cell = self.ydoc.get_map(cell_id)
            cell_data = {
                "id": cell_id,
                "cell_type": cell.get("type"),
                "source": cell.get("source").__str__().split("\n"),
                "outputs": [output for output in cell.get("outputs")],
                "metadata": {
                    "gm": {
                        "top": cell.get("top"),
                        "left": cell.get("left"),
                        "height": cell.get("height"),
                        "width": cell.get("width"),
                        "collapsed": cell.get("collapsed"),
                    }
                },
            }
            notebook["cells"].append(cell_data)

        # Collect np_graph and pc_graph
        for id in self.ynp_graph.keys():
            notebook["metadata"]["gm"]["np_graph"][id] = [
                next_id for next_id in self.ynp_graph.get(id)
            ]
        for id in self.ypc_graph.keys():
            notebook["metadata"]["gm"]["pc_graph"][id] = [
                child_id for child_id in self.ypc_graph.get(id)
            ]

        # Save to file
        # add .ganimede before .ipynb
        notebook_path = Path(self.notebook_path)
        notebook_path = notebook_path.parent / (notebook_path.stem + ".ganimede.ipynb")
        with open(notebook_path, "w") as f:
            json.dump(notebook, f)


def _generate_random_cell_id(id_length: int = 8) -> str:
    n_bytes = max(id_length * 3 // 4, 1)
    return urlsafe_b64encode(urandom(n_bytes)).decode("ascii").rstrip("=")
