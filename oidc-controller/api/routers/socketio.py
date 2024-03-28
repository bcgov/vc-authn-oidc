import socketio # For using websockets
import logging
import time

logger = logging.getLogger(__name__)


connections = {}

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

sio_app = socketio.ASGIApp(socketio_server=sio, socketio_path='/ws/socket.io')

@sio.event
async def connect(sid, socket):
    logger.info(f">>> connect : sid={sid}")

@sio.event
async def initialize(sid, data):
    global connections
    # Store websocket session matched to the presentation exchange id 
    connections[data.get('pid')] = sid

@sio.event
async def disconnect(sid):
    global connections
    logger.info(f">>> disconnect : sid={sid}")
    # Remove websocket session from the store
    if len(connections) > 0:
        connections = {k:v for k,v in connections.items() if v != sid}

def connections_reload():
    global connections
    return connections