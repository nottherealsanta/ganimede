// create a websocket svelte store 

// import { writable } from "svelte/store";
import { notebook } from "./notebook";

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
            socket.send(JSON.stringify({
                "channel": "status",
                "message": "socket_ready"
            }));
            console.log("Socket opened");
        };
        socket.onclose = function (event) {
            console.log("Socket closed");
            socket = null;
        }
        socket.onmessage = function (event) {
            console.log("Socket message: ", event.data);
            let message = JSON.parse(event.data);
            if (message["channel"] === "notebook") {
                notebook.set(message["message"]);
            }
        };

    };
}

export async function send_message(channel = "status"
    , message) {
    if (socket === null) {
        await open_socket();
    }
    socket.send(JSON.stringify({
        "channel": channel,
        "message": message
    }));
}