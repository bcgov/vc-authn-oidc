const io = require("socket.io-client");

function App() {
  const socket = io("ws://localhost:5100/", {
    path: "/ws/",
    autoConnect: false,
  });

  socket.connect();

  socket.on("connect", () => console.log("Connected"));

  socket.on("message", (e) => console.log("Received", e));
}

App();
