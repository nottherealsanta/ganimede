from ganimede.main import main, dev_main
import webview
import subprocess
import time
import sys
import os


def run_uvicorn():
    # Use sys.executable to ensure we're using the correct Python interpreter
    uvicorn_process = subprocess.Popen(
        [sys.executable, "-c", "from ganimede.main import dev_main; dev_main()"]
    )
    return uvicorn_process


if __name__ == "__main__":
    # Start uvicorn in a subprocess
    uvicorn_process = run_uvicorn()

    # Give uvicorn a moment to start up
    time.sleep(2)

    # Start webview in the main thread
    webview.create_window("Ganimede", "http://localhost:8000")
    webview.start()

    # Cleanup: terminate the uvicorn process when webview closes
    uvicorn_process.terminate()

    # On Windows, we need to forcefully kill the process
    if os.name == "nt":
        os.kill(uvicorn_process.pid, signal.SIGTERM)

    uvicorn_process.wait()
