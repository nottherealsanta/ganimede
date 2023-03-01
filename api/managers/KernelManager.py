import queue
import asyncio

from jupyter_client import AsyncKernelManager
from starlette.responses import JSONResponse
from rich import print

import logging

logging.basicConfig(level=logging.DEBUG)


class KernelManger:
    def __init__(self):
        logging.debug("Initializing KernelManger")
        self.kernel_manager = AsyncKernelManager()
        self.kernel_client = None

    def __del__(self) -> None:
        print("shutting down kernel")
        # self.kernel_manager.shutdown_kernel()
        if self.kernel_client:
            self.kernel_client.stop_channels()
            self.kernel_client.close()

    async def start_kernel(self):
        logging.debug("Starting kernel")

        if self.kernel_client is not None:
            logging.debug("Kernel already started")
            return

        try:
            await self.kernel_manager.start_kernel()
            self.kernel_client = self.kernel_manager.client()
            await self.kernel_client.start_channels()
        except Exception as e:
            logging.error(e)
            self.kernel_client = None

        logging.debug("Kernel started")

    async def flush_io_pub(self):
        while True:
            try:
                await self.kernel_client.get_iopub_msg(timeout=0.1)
            except queue.Empty:
                logging.debug("No more messages")
                break

    async def execute(
        self, code: str, output_queue: queue.Queue = None
    ) -> JSONResponse:
        logging.debug(f"Executing: {code}")

        if self.kernel_client is None:
            logging.debug("Kernel not started")
            # await self.start_kernel()
            # return

        await self.flush_io_pub()

        async def execute_code(code: str) -> None:
            code = "".join(code)
            self.kernel_client.execute(code)
            client_execute_reply = await self.kernel_client.get_shell_msg()
            logging.debug(f"client_execute_reply: {client_execute_reply}")

        async def get_output() -> None:
            while True:
                try:
                    msg = await self.kernel_client.get_iopub_msg(timeout=0.1)
                    logging.debug(f"msg: {msg}")
                    output_queue.put_nowait(msg)
                except queue.Empty:
                    logging.debug("No more messages")
                    break

        loop = asyncio.get_event_loop()

        execute_task = loop.create_task(execute_code(code))
        output_task = loop.create_task(get_output())

        await asyncio.wait([execute_task, output_task])

        logging.debug("Execution finished")
        return JSONResponse({"status": "ok"})
