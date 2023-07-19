import socketio # For using websockets
import logging

logger = logging.getLogger(__name__)


connections = {}

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

sio_app = socketio.ASGIApp(socketio_server=sio)

@sio.event
async def connect(sid, socket):
    # logger.info(f">>> connect : sid={sid}")
    # logger.info(f">>> connect : socket={socket}")
    await sio.emit('message', {'data': "I'm a real boy!"})
    # TODO: Add the sid 

@sio.event
async def initialize(sid, data):
    logger.info(f">>> initialize : sid={sid}")
    logger.info(f">>> initialize : pid={data.get('pid')}")
    # TODO: Add the pid to the acapy_handler.connections dict

@sio.event
async def disconnect(sid):
    logger.info(f">>> disconnect : sid={sid}")
    # TODO: Remove the sid,pid from the connections dict
