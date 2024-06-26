import uvicorn
from starlette.applications import Starlette
from starlette.responses import FileResponse, PlainTextResponse
from starlette.routing import Route
from pathlib import Path
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

FRONTEND_DIR = Path("../../frontend").resolve()
MONACO_DIR = FRONTEND_DIR / "node_modules" / "monaco-editor" / "esm" / "vs"


async def serve_file(request):
    try:
        # Use request.url.path instead of request.path
        relative_path = request.url.path.lstrip("/")
        possible_paths = [
            FRONTEND_DIR / relative_path,
            FRONTEND_DIR / "dist" / relative_path,
            MONACO_DIR
            / Path(relative_path).relative_to("node_modules/monaco-editor/esm/vs"),
        ]

        for file_path in possible_paths:
            logger.debug(f"Attempting to serve file: {file_path}")
            if file_path.exists() and file_path.is_file():
                logger.info(f"Serving file: {file_path}")
                return FileResponse(file_path)

        logger.warning(f"File not found: {relative_path}")
        return PlainTextResponse(f"File not found: {relative_path}", status_code=404)
    except Exception as e:
        logger.error(f"Error serving file: {str(e)}")
        logger.error(traceback.format_exc())
        return PlainTextResponse(f"Internal server error: {str(e)}", status_code=500)


async def homepage(request):
    try:
        return FileResponse(FRONTEND_DIR / "index.html")
    except Exception as e:
        logger.error(f"Error serving homepage: {str(e)}")
        logger.error(traceback.format_exc())
        return PlainTextResponse(f"Internal server error: {str(e)}", status_code=500)


routes = [
    Route("/", endpoint=homepage),
    Route("/{path:path}", endpoint=serve_file),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    logger.info(f"Frontend directory: {FRONTEND_DIR}")
    logger.info(f"Monaco directory: {MONACO_DIR}")
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
