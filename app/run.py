import asyncio
import multiprocessing
import signal
import sys
import traceback
import uvicorn

from app.core import Live2dAI
from app.utils.config import CONFIG


def run_app_server(config):
    uvicorn.run(
        "app.main:app",
        host=config.ip,
        port=config.port,
        access_log=False,
        workers=10,
        log_level="info"
    )

def run_server():
    multiprocessing.freeze_support()
    app_server_process = multiprocessing.Process(
        target=run_app_server, args=(CONFIG,)
    )
    app_server_process.start()

    model_repository = Live2dAI()

    def shutdown(signum, frame):
        print(f"Received signal {signum}, terminating FastAPI process...")
        app_server_process.terminate()
        app_server_process.join(timeout=3)
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    try:
        asyncio.run(model_repository.start())
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    except Exception as e:
        print(f"Error running server: {e}, {traceback.format_exc()}")
    finally:
        shutdown(signal.SIGINT, None)
        print("supervisor has shut down.")
    pass

if __name__ == "__main__":
    run_server()