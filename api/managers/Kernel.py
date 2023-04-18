import queue
import asyncio

from jupyter_client import AsyncKernelManager
from starlette.responses import JSONResponse
from rich import print

import logging

from managers.Comms import Comms

log = logging.getLogger(__name__)


class Kernel:
    def __init__(self, comms: Comms):
        log.debug("Initializing Kernel")
        self.kernel_manager = AsyncKernelManager()
        self.kernel_client = None
        self.run_queue = asyncio.Queue()

        self._busy = False

        self.comms_queue = comms.channel_queues["kernel"]

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

    # getter and setting for busy
    @property
    def busy(self):
        return self._busy

    @busy.setter
    def busy(self, value):
        self._busy = value

    def __del__(self) -> None:
        log.debug("Shutting down kernel")
        # self.kernel_manager.shutdown_kernel()
        # if self.kernel_client:
        #     self.kernel_client.stop_channels()
        #     self.kernel_client.close()

    async def start_kernel(self):
        log.debug("Starting kernel")

        if self.kernel_client is not None:
            log.debug("Kernel already started")
            return

        try:
            await self.kernel_manager.start_kernel()
            self.kernel_client = self.kernel_manager.client()
            self.kernel_client.start_channels()
            # TODO: check if kernel is ready
        except Exception as e:
            log.error(e)
            self.kernel_client = None

        log.debug("Kernel started")
        log.debug(f"Kernel client: {self.kernel_client}")

    async def flush_io_pub(self):
        while True:
            try:
                await self.kernel_client.get_iopub_msg(timeout=0.1)
            except queue.Empty:
                log.debug("No more messages")
                break

    def _msg_to_output(self, msg):
        output = {
            "output_type": msg["msg_type"],
        }

        # TODO: handle other output types
        if "text" in msg["content"]:
            output["text"] = [msg["content"]["text"]]
        if "data" in msg["content"]:
            output["data"] = msg["content"]["data"]
        if "metadata" in msg["content"]:
            output["metadata"] = msg["content"]["metadata"]
        if "name" in msg["content"]:
            output["name"] = msg["content"]["name"]
        if "traceback" in msg["content"]:
            output["traceback"] = msg["content"]["traceback"]

        return output

    async def execute(self, code: str, msg_queue: asyncio.Queue):
        log.debug(f"executing: {code}")

        if self.kernel_client is None:
            log.debug("Kernel not started")
            await self.start_kernel()
            log.debug(f"Kernel client: {self.kernel_client}")

        await self.flush_io_pub()

        async def execute_code(code: str) -> None:
            code = "\n".join(code)
            self.kernel_client.execute(code)
            client_execute_reply = await self.kernel_client.get_shell_msg()
            log.debug(f"client_execute_reply: {client_execute_reply}")

        async def proc_io_msgs() -> None:
            self.busy = True
            while self.busy:
                try:
                    msg = await self.kernel_client.get_iopub_msg(timeout=1)

                    #
                    # msg_type is only available non-outputs
                    #
                    if msg["msg_type"] == "status":
                        if msg["content"]["execution_state"] == "idle":
                            self.busy = False
                        msg = {
                            "msg_type": "status",
                            "execution_state": msg["content"]["execution_state"],
                        }
                    elif msg["msg_type"] == "execute_input":
                        msg = {
                            "msg_type": "execute_input",
                        }
                    else:
                        msg = self._msg_to_output(msg)

                    msg_queue.put_nowait(msg)
                    log.debug(f"+msg_queue size: {msg_queue.qsize()}")
                except queue.Empty:
                    log.debug("msg_queue empty")
                    pass

        loop = asyncio.get_event_loop()

        execute_task = loop.create_task(execute_code(code))
        output_task = loop.create_task(proc_io_msgs())

        await asyncio.gather(execute_task, output_task)

        log.debug("Execution finished")
        return execute_task.result()
