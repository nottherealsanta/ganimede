import logging
import traceback
from pathlib import Path
import uvicorn
from starlette.applications import Starlette
from starlette.responses import FileResponse, PlainTextResponse
from starlette.routing import Route, WebSocketRoute

from comms import Comms

# Set up logging with DEBUG level to capture detailed information during development
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the directories for serving files
FRONTEND_DIR = Path(
    "../../frontend"
).resolve()  # Resolve the absolute path for the frontend directory
MONACO_DIR = (
    FRONTEND_DIR / "node_modules" / "monaco-editor" / "esm" / "vs"
)  # Path to the Monaco editor's files


# COMMS

comms = Comms()


# ROUTES


# -- Function to serve files based on the request URL
async def serve_file(request):
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
        ]

        # Attempt to find and serve the requested file from the possible paths
        for file_path in possible_paths:
            logger.debug(f"Attempting to serve file: {file_path}")
            if file_path.exists() and file_path.is_file():
                logger.info(f"Serving file: {file_path}")
                return FileResponse(file_path)

        # If the file is not found, log a warning and return a 404 response
        logger.warning(f"File not found: {relative_path}")
        return PlainTextResponse(f"File not found: {relative_path}", status_code=404)
    except Exception as e:
        # Log any exceptions that occur and return a 500 response
        logger.error(f"Error serving file: {str(e)}")
        logger.error(traceback.format_exc())
        return PlainTextResponse(f"Internal server error: {str(e)}", status_code=500)


# -- Function to serve the homepage
async def homepage(request):
    try:
        # Attempt to serve the index.html file as the homepage
        return FileResponse(FRONTEND_DIR / "index.html")
    except Exception as e:
        # Log any exceptions that occur and return a 500 response
        logger.error(f"Error serving homepage: {str(e)}")
        logger.error(traceback.format_exc())
        return PlainTextResponse(f"Internal server error: {str(e)}", status_code=500)


# -- Define the routes for the web p
routes = [
    Route("/", endpoint=homepage),  # Route for the homepage
    Route("/{path:path}", endpoint=serve_file),  # Route for serving files
    WebSocketRoute("/", comms.endpoint),  # Route for the WebSocket
]

# -- Create the Starlette application with debugging enabled and the defined routes
app = Starlette(debug=True, routes=routes)


# Main entry point for running the application with Uvicorn
if __name__ == "__main__":
    # Log the paths being served
    logger.info(f"Frontend directory: {FRONTEND_DIR}")
    logger.info(f"Monaco directory: {MONACO_DIR}")
    # Run the application with Uvicorn, listening on all interfaces at port 8000, with debug logging and auto-reload enabled
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
