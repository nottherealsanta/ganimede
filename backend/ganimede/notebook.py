from os import getcwd
import json
import asyncio
import queue
import logging
from pathlib import Path
import y_py as Y
from os import urandom
from base64 import urlsafe_b64encode
import sqlite3
from os import path

from kernel import Kernel
from comms import Comms

log = logging.getLogger(__name__)


class Notebook:
    def __init__(
        self,
        comms: Comms,
        ydoc: Y.YDoc,
        # notebook_path: str,
    ):
        self.comms = comms
        self.ydoc = ydoc
        self.kernel = Kernel(comms, ydoc)

        # websocket message queue
        self.comms_queue = comms.channel_queues["notebook"]
        asyncio.create_task(self.listen_comms())

        self.run_queue = asyncio.Queue()
        asyncio.create_task(self.run_queue_loop())
        self.yrun_queue = self.ydoc.get_array("run_queue")

        self.create_db()

    def create_db(self):
        log.info("table notebooks created")

    async def open(self, path: str):
        log.info("LOAD notebook")

        # read file
        try:
            with open(path, "r") as f:
                content = f.read()
        except Exception as e:
            log.error(f"Error reading file: {e}")
            return

        file_name = path.split("/")[-1]

        # remove suffix
        file_name = file_name.split(".")[0]

        # set notebook path
        with self.ydoc.begin_transaction() as t:
            self.ydoc.get_text("nb_path").delete_range(
                t, 0, len(self.ydoc.get_text("nb_path"))
            )
            self.ydoc.get_text("nb_path").insert(t, 0, file_name)

        # set notebook file
        self.notebook_id = _generate_random_id()
        self.init_cells_from_content(content)

        await self.empty_run_queue()

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

    def init_cells_from_content(self, content: str):
        content = json.loads(content)
        ## y
        self.ycells = self.ydoc.get_array("cells")
        # delete all cells
        with self.ydoc.begin_transaction() as t:
            self.ycells.delete_range(t, 0, len(self.ycells))

        # heading level function
        def calculate_heading_level(cell):
            if cell["cell_type"] == "markdown":
                content = "".join(cell["source"])
                lines = content.split("\n")

                for line in lines:
                    stripped_line = line.strip()
                    if stripped_line.startswith("#"):
                        # Count the number of consecutive '#' at the start
                        heading_level = len(stripped_line) - len(
                            stripped_line.lstrip("#")
                        )
                        if heading_level > 0 and stripped_line[heading_level] in [
                            " ",
                            "\t",
                        ]:
                            return heading_level

            return None

        ### set from juptyer notebook
        for cell in content["cells"]:
            id = cell["id"] if "id" in cell else _generate_random_id()
            source = Y.YText(("".join(cell["source"])))
            outputs = Y.YArray(cell["outputs"] if "outputs" in cell else [])
            # if cell["cell_type"] == "markdown":
            #     heading_level = (
            #         1 if "".join(cell["source"]).split("\n")[0].startswith("#") else 0
            #     )
            #     heading_level = None if heading_level == 0 else heading_level
            # else:
            #     heading_level = None
            heading_level = calculate_heading_level(cell)
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
                ycell.set(t, "heading_level", heading_level)

                ycell.set(
                    t,
                    "collapsed",
                    None,
                )  # i, o, b, h
                ycell.set(
                    t,
                    "parent_collapsed",
                    False,
                )
                ycell.set(t, "state", "idle")  # idle, running, queued, done
                ycell.set(t, "execution_time", None)
                # ycells
                self.ycells.append(t, id)

    async def queue_cell(self, cell_id: str):
        log.debug(f"queue_cell: {cell_id}")
        self.run_queue.put_nowait((cell_id))
        self._change_cell_state(cell_id, "queued")
        with self.ydoc.begin_transaction() as t:
            self.ydoc.get_array("run_queue").append(t, cell_id)

    async def interrupt_kernel(self):
        await self.empty_run_queue()
        await self.kernel.interrupt()

    async def run_queue_loop(self):
        while True:
            cell_id = await self.run_queue.get()
            self._change_cell_state(cell_id, "running")
            self._clear_outputs(cell_id)
            await self.run(cell_id)

            # delete from queue after run
            with self.ydoc.begin_transaction() as t:
                if len(self.ydoc.get_array("run_queue")) > 0:
                    self.ydoc.get_array("run_queue").delete(t, 0)

            # # insert cell to db
            # await self.insert_cell(cell_id)

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

            log.info(f"msg: {msg}")
            log.info(f"-msg_queue size: {msg_queue.qsize()}")

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
                    log.info(f"appending msg: {msg}")
                    self.ydoc.get_map(cell_id).get("outputs").append(t, msg)

        self._change_cell_state(cell_id, "idle")

    async def checkpoint(self):
        log.info("CHECKPOINT notebook")


def _generate_random_id(id_length: int = 8) -> str:
    n_bytes = max(id_length * 3 // 4, 1)
    return urlsafe_b64encode(urandom(n_bytes)).decode("ascii").rstrip("=")
