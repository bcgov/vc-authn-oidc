import logging
import os
import time
from pathlib import Path

import uvicorn
from api.core.config import settings
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import socketio # For using websockets

print('here is the ws stuff', socketio)

from .routers import acapy_handler, oidc, presentation_request, well_known_oid_config
from .verificationConfigs.router import router as ver_configs_router
from .clientConfigurations.router import router as client_config_router
from .db.session import init_db, get_db

from api.core.oidc.provider import init_provider

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

##################################
# Configure the websocket
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, socket):
    print('connected', sid)
    await sio.emit('message', {'data': "I'm a real boy!"})

@sio.event
def disconnected(sid):
    print('disconnected', sid)

sio_app = socketio.ASGIApp(socketio_server=sio)

app.mount('/ws', sio_app)
##################################

origins = ["*"]

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


##################################
# Test the websocket
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Socket.io Test</title>
    <script src="https://cdn.socket.io/4.3.2/socket.io.min.js"></script>
    <script>
        const socket = io("ws://localhost:5000", {
        path: "/ws/socket.io",
        autoConnect: false,
        });

        const handleConnect = () => {
            console.log("Button Clicked to Connect");
            socket.connect();
        };

        const handleDisconnect = () => {
            console.log("Button Clicked to Disconnect");
            socket.disconnect();
        };

        socket.on("message", (e) => console.log("Received", e));
    </script>
</head>
<body>
    <div className="App">
        <button onClick="handleConnect()">Connect</button>
        <button onClick="handleDisconnect()">Disconnect</button>
    </div>
</body>
</html>
"""

@app.get("/test-ws")
async def root():
    return HTMLResponse(html)
##################################

@app.on_event("startup")
async def on_tenant_startup():
    """Register any events we need to respond to."""
    await init_db()
    await init_provider(await get_db())
    logger.warning(">>> Starting up app ...")


@app.on_event("shutdown")
def on_tenant_shutdown():
    """TODO no-op for now."""
    logger.warning(">>> Shutting down app ...")


@app.get("/", tags=["liveness", "readiness"])
@app.get("/health", tags=["liveness", "readiness"])
def main():
    return {"status": "ok", "health": "ok"}


if __name__ == "__main__":
    print("main.")
    uvicorn.run(app, host="0.0.0.0", port=5100)
