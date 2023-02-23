import logging
import os
import time
from pathlib import Path

import uvicorn
from api.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import acapy_handler, oidc, presentation_request, well_known_oid_config
from .verificationConfigs.router import router as ver_configs_router

# setup loggers
# TODO: set config via env parameters...
logging_file_path = (Path(__file__).parent / "logging.conf").resolve()
logging.config.fileConfig(logging_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

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

app.include_router(well_known_oid_config.router, include_in_schema=True)

# TWo paths, one deprecated
app.include_router(oidc.router, tags=["oidc"], include_in_schema=False)
app.include_router(oidc.router, prefix="/vc/connect", tags=["oidc-deprecated"], include_in_schema=False)

app.include_router(acapy_handler.router, prefix="/webhooks", include_in_schema=False)
app.include_router(presentation_request.router, include_in_schema=False)

origins = ["*"]

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def on_tenant_startup():
    """Register any events we need to respond to."""
    logger.warning(">>> Starting up app ...")


@app.on_event("shutdown")
def on_tenant_shutdown():
    """TODO no-op for now."""
    logger.warning(">>> Shutting down app ...")


@app.get("/", tags=["liveness"])
def main():
    return {"status": "ok", "health": "ok"}


if __name__ == "__main__":
    print("main.")
    uvicorn.run(app, host="0.0.0.0", port=5100)
