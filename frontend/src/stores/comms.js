export let socket = null;

export async function open_socket() {
  console.log("Opening socket");
  if (socket === null) {
    socket = new WebSocket("ws://localhost:8000/");
    socket.onopen = async function (event) {
      while (socket.readyState !== WebSocket.OPEN) {
        console.log("Waiting for socket to open");
        await new Promise(r => setTimeout(r, 100));

      }
      // socket.send(JSON.stringify({
      //   "channel": "notebook",
      //   "method": "get",
      // }));
      console.log("Socket opened");
      socket.ready = true;
    };
    socket.onclose = function (event) {
      socket.ready = false;
      socket = null;
      console.log("Socket closed");
    }
  }
};

export async function send_message({ channel, method, message }) {
  console.log("send : ", { channel, method, message });
  if (socket === null) {
    open_socket();
    throw new Error("Socket is not initialized.");
  }
  socket.send(JSON.stringify({
    "channel": channel,
    "method": method,
    "message": message
  }));
}