# import api.core.logconfig
import logging
import logging.config
import structlog
import os
import time
import uuid
from pathlib import Path

import uvicorn
from api.core.config import settings
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .routers import acapy_handler, oidc, presentation_request, well_known_oid_config
from .verificationConfigs.router import router as ver_configs_router
from .clientConfigurations.router import router as client_config_router
from .db.session import init_db, get_db
from .routers.socketio import sio_app

from api.core.oidc.provider import init_provider

logger: structlog.typing.FilteringBoundLogger = structlog.getLogger(__name__)

# Setup loggers
logging_file_path = os.environ.get(
    "LOG_CONFIG_PATH", (Path(__file__).parent / "logging.conf").resolve()
)


os.environ["TZ"] = settings.TIMEZONE
time.tzset()


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
        # middleware=None,
    )
    return application


app = get_application()
app.include_router(ver_configs_router, prefix="/ver_configs", tags=["ver_configs"])
app.include_router(client_config_router, prefix="/clients", tags=["oidc_clients"])
app.include_router(well_known_oid_config.router, tags=[".well-known"])
app.include_router(
    oidc.router, tags=["OpenID Connect Provider"], include_in_schema=False
)
app.include_router(acapy_handler.router, prefix="/webhooks", include_in_schema=False)
app.include_router(presentation_request.router, include_in_schema=False)

# DEPRECATED PATHS - For backwards compatibility with vc-authn-oidc 1.0
app.include_router(
    oidc.router, prefix="/vc/connect", tags=["oidc-deprecated"], include_in_schema=False
)

# Connect the websocket server to run within the FastAPI app
app.mount("/ws", sio_app)

origins = ["*"]

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    # clear the threadlocal context
    structlog.threadlocal.clear_threadlocal()
    # bind threadlocal
    structlog.threadlocal.bind_threadlocal(
        logger="uvicorn.access",
        request_id=str(uuid.uuid4()),
        cookies=request.cookies,
        scope=request.scope,
        url=str(request.url),
    )
    start_time = time.time()
    try:
        response: Response = await call_next(request)
    finally:
        process_time = time.time() - start_time
        logger.info(
            "processed a request",
            status_code=response.status_code,
            process_time=process_time,
        )
    return response


@app.on_event("startup")
async def on_tenant_startup():
    """Register any events we need to respond to."""
    await init_db()
    await init_provider(await get_db())
    logger.info(">>> Starting up app new ...")


@app.on_event("shutdown")
def on_tenant_shutdown():
    """TODO no-op for now."""
    logger.warning(">>> Shutting down app ...")


@app.get("/", tags=["liveness", "readiness"])
@app.get("/health", tags=["liveness", "readiness"])
def main():
    return {"status": "ok", "health": "ok"}


if __name__ == "__main__":
    logger.info("main.")
    uvicorn.run(app, host="0.0.0.0", port=5100)
