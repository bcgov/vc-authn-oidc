import socketio # For using websockets
import logging

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
    connections[data.get('pid')] = sid
    print("connections from socketio.py", connections)

@sio.event
async def disconnect(sid):
    global connections
    logger.info(f">>> disconnect : sid={sid}")
    connections = {k:v for k,v in connections.items() if v != sid}
