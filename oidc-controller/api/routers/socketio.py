import socketio # For using websockets
import logging
import time

logger = logging.getLogger(__name__)


connections = {}

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

sio_app = socketio.ASGIApp(socketio_server=sio)

@sio.event
async def connect(sid, socket):
    await sio.emit('message', {'data': "I'm a real boy!"})

@sio.event
async def initialize(sid, data):
    global connections

    logger.info(f">>> initialize : sid={sid}")
    logger.info(f">>> initialize : pid={data.get('pid')}")

    # Store websocket session matched to the presentation exchange id 
    connections[data.get('pid')] = sid
    # TODO: This isn't doing what I wanted
    # await sio.save_session(sid, {'pid': data.get('pid')})
    # print("connections from socketio.py", connections)

@sio.event
async def disconnect(sid):
    global connections
    logger.info(f">>> disconnect : sid={sid}")
    if len(connections) > 0:
        connections = {k:v for k,v in connections.items() if v != sid}

def connections_reload():
    global connections
    return connections