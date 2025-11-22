from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cdn_host import monkey_patch_for_docs_ui

from app.database import init_db
from app.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = aiohttp.ClientSession()
    await init_db()
    yield
    await app.state.http_client.close()
    

app = FastAPI(
    title="model-repository",
    lifespan=lifespan,
    response_model_exclude_unset=True,
    version="1.0.0",
)

monkey_patch_for_docs_ui(app)

app.include_router(api_router)

app.mount("/static", StaticFiles(directory="resource/static"), name="static")