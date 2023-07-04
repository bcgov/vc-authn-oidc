import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import socketio # Installed with 'pip install python-socketio`

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Socket.io Test</title>
    <script src="https://cdn.socket.io/4.3.2/socket.io.min.js"></script>
    <script>
        const socket = io("ws://localhost:5100", {
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

# Create a FastAPI instance
app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse(html)

# Create a test websocket server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, socket):
    print('connected', sid)
    await sio.emit('message', {'data': "I'm a real boy!'"})

@sio.event
def disconnected(sid):
    print('disconnected', sid)

sio_app = socketio.ASGIApp(socketio_server=sio)

app.mount('/ws', sio_app)

uvicorn.run(app, host="localhost", port=5100)