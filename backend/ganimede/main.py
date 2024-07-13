import logging
import traceback
from pathlib import Path
import asyncio

from rich.logging import RichHandler

import uvicorn
from starlette.applications import Starlette
from starlette.responses import FileResponse, PlainTextResponse, JSONResponse
from starlette.routing import Route, WebSocketRoute

import y_py as Y
from websockets import serve, connect
from ypy_websocket import ASGIServer, WebsocketServer, WebsocketProvider

from ganimede.comms import Comms
from ganimede.notebook import Notebook

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)

# Define the directories for serving files
DEV = True
FRONTEND_DIR = Path(
    "../frontend"
).resolve()  # Resolve the absolute path for the frontend directory
MONACO_DIR = FRONTEND_DIR / "node_modules" / "monaco-editor" / "esm" / "vs"


# Y PY

# -- yapp server
websocket_server = WebsocketServer()
# yapp = ASGIServer(websocket_server)
ydoc = Y.YDoc()


# -- yapp server task
async def ypy_ws_server_start():
    async with (
        WebsocketServer(log=logger) as websocket_server,
        serve(
            websocket_server.serve, "localhost", 1234, close_timeout=1, max_size=2**24
        ),
    ):
        logger.info("Y PY websocket server started")
        await asyncio.Future()  # run forever


# COMMS

comms = Comms()

# NOTEBOOK

notebook = None

# ROUTES


# -- serve files based on the request URL
async def serve_file(request):
    print(f"Request URL: {request.url}")
    try:
        # Extract the relative path from the request URL
        relative_path = request.url.path.lstrip("/")
        # Define possible paths for the requested file
        possible_paths = [
            FRONTEND_DIR / relative_path,  # Direct path in the frontend directory
            FRONTEND_DIR / "dist" / relative_path,  # Path within the dist folder
            MONACO_DIR
            / Path(relative_path).relative_to(
                "node_modules/monaco-editor/esm/vs"
            ),  # Path for Monaco editor files
            # MONACO_DIR
            # / relative_path,
        ]

        # Attempt to find and serve the requested file from the possible paths
        for file_path in possible_paths:

            logger.debug(f"Attempting to serve file: {file_path}")
            if file_path.exists() and file_path.is_file():
                logger.debug(f"Serving file: {file_path}")
                return FileResponse(file_path)

        # If the file is not found, log a warning and return a 404 response
        logger.warning(f"File not found: {relative_path}")
        return PlainTextResponse(f"File not found: {relative_path}", status_code=404)
    except Exception as e:
        # Log any exceptions that occur and return a 500 response
        logger.error(f"Error serving file: {str(e)}")
        logger.error(traceback.format_exc())
        return PlainTextResponse(f"Internal server error: {str(e)}", status_code=500)


# -- serve the homepage
async def homepage(request):

    global notebook

    if notebook is None:
        notebook = Notebook(comms=comms, ydoc=ydoc)
        if DEV:
            logger.info("Opening test notebook")
            await open_notebook(
                ""
            )  # TODO: remove this to open notebooks from the frontend

    try:
        # Attempt to serve the index.html file as the homepage
        # if DEV:
        logger.info(f"Serving dev homepage: {FRONTEND_DIR / 'dev_index.html'}")
        return FileResponse(FRONTEND_DIR / "dev_index.html")
        # return FileResponse(FRONTEND_DIR / "index.html")
    except Exception as e:
        # Log any exceptions that occur and return a 500 response
        logger.error(f"Error serving homepage: {str(e)}")
        logger.error(traceback.format_exc())
        return PlainTextResponse(f"Internal server error: {str(e)}", status_code=500)


# -- serve the file browser
async def file_browser(request):
    """
    request comes with a query for a path
    return a list of visible files/folders in the path, including their names and types
    """
    path = request.query_params.get("path", "")
    if path == "":
        path = Path.home()
    else:
        path = Path(str(Path.home()) + "/" + path)

    if path.exists():
        if path.is_dir():
            # List visible files and folders with their types
            contents = [
                {"name": f.name, "type": "folder" if f.is_dir() else "file"}
                for f in path.iterdir()
                if not f.name.startswith(".")
            ]
            return JSONResponse({"contents": contents})
        else:
            # If it's a visible file, return its name and type
            if not path.name.startswith("."):
                return JSONResponse({"contents": [{"name": path.name, "type": "file"}]})
            else:
                return JSONResponse({"contents": []})
    else:
        return JSONResponse({"contents": []})


# -- open a notebook
async def open_notebook(request):
    """
    request comes with a query for a path
    return the content of the file
    """
    # TODO
    if DEV:
        path = "repos/ganimede/tests/test_notebook.ipynb"  #
    else:
        path = request.query_params.get("path", "")
    logger.info(f"Opening notebook: {path}")
    if path == "":
        return JSONResponse({"error": "No path provided"})
    else:
        home_dir_path = str(Path.home())
        await notebook.open(home_dir_path + "/" + path)

    return JSONResponse({"status": "ok"})


async def startup():

    logger.info("Starting up")

    # starting YPY websocket server
    loop = asyncio.get_event_loop()
    _task = loop.create_task(ypy_ws_server_start())
    await asyncio.sleep(0.5)  # wait for server to start
    websocket = await connect("ws://localhost:1234/g-y-room", max_size=2**24)
    websocket_provider = WebsocketProvider(ydoc, websocket, log=logger)
    task = asyncio.create_task(websocket_provider.start())
    await websocket_provider.started.wait()


# -- Define the routes for the web p
routes = [
    Route("/", endpoint=homepage),  # Route for the homepage
    Route("/file_browser", endpoint=file_browser),
    Route("/open_notebook", endpoint=open_notebook),
    Route("/{path:path}", endpoint=serve_file),  # Route for serving files
    WebSocketRoute("/", comms.endpoint),  # Route for the WebSocket
]

# -- Create the Starlette application with debugging enabled and the defined routes
app = Starlette(debug=True, routes=routes, on_startup=[startup])


def dev_main():
    global DEV
    DEV = True
    logger.info("Starting up in dev mode")

    # Log the paths being served
    global FRONTEND_DIR, MONACO_DIR
    FRONTEND_DIR = Path(
        "../../frontend"
    ).resolve()  # Resolve the absolute path for the frontend directory
    MONACO_DIR = FRONTEND_DIR / "node_modules" / "monaco-editor" / "esm" / "vs"
    logger.info(f"Frontend directory: {FRONTEND_DIR}")
    logger.info(f"Monaco directory: {MONACO_DIR}")

    # Run the application with Uvicorn, listening on all interfaces at port 8000, with debug logging and auto-reload enabled
    uvicorn.run(
        app="ganimede.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


def main():
    global FRONTEND_DIR, MONACO_DIR
    FRONTEND_DIR = Path(
        "../frontend/dist"
    ).resolve()  # Resolve the absolute path for the frontend directory
    MONACO_DIR = FRONTEND_DIR  # Path to the Monaco editor's files

    # Run the application with Uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)


# Main entry point for running the application with Uvicorn
if __name__ == "__main__":
    dev_main()
