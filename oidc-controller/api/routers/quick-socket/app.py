import uvicorn
from fastapi import FastAPI
import socketio # Installed with 'pip install python-socketio`

# Create a FastAPI instance
app = FastAPI()

# Create a test websocket server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app.mount('/wd', sio)

@sio.event
def connect(sid, socket):
    print('connected', sid)

@sio.event
def disconnected(sid):
    print('disconnected', sid)

@sio.event
def get_name(sid, data):
    print('get_name', data)
    sio.emit('name', data)

uvicorn.run(app, host="0.0.0.0", port=5100)

# TODO1: Test with websocat
# TODO2: Integrate into acapy_handler.py