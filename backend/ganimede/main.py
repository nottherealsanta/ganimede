import uvicorn
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Route


async def homepage(request):
    return FileResponse("../../frontend/index.html")


routes = [
    Route("/", endpoint=homepage),
]


app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(
        app=f"main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False,
    )
