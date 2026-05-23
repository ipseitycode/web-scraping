import importlib
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from shared.security.api_key_middleware import ApiKeyMiddleware
from shared.exception.base_exception import BaseApiException

_ROOT = Path(__file__).parent
_EXCLUDED = {"shared", "venv", ".venv", "node_modules"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    for path in _ROOT.glob("*/*/jobs.py"):
        rel = path.relative_to(_ROOT)
        if rel.parts[0] not in _EXCLUDED:
            module_path = rel.with_suffix("").as_posix().replace("/", ".")
            module = importlib.import_module(module_path)
            if hasattr(module, "register_jobs"):
                module.register_jobs(scheduler)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(ApiKeyMiddleware)


@app.exception_handler(BaseApiException)
async def handle_api_exception(request: Request, exc: BaseApiException):
    return JSONResponse(status_code=422, content=exc.response)


for _path in _ROOT.glob("*/*/main.py"):
    _rel = _path.relative_to(_ROOT)
    if _rel.parts[0] not in _EXCLUDED:
        _module_path = _rel.with_suffix("").as_posix().replace("/", ".")
        _module = importlib.import_module(_module_path)
        if hasattr(_module, "router"):
            app.include_router(_module.router, prefix="/web-scraping")
