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
                "channel": "notebook",
                "method": "get",
            }));
            console.log("Socket opened");
        };
        socket.onclose = function (event) {
            console.log("Socket closed");
            socket = null;
        }
        socket.onmessage = function (event) {
            console.log("Socket message: ", JSON.parse(event.data));
            let message = JSON.parse(event.data);
            if (message["channel"] === "notebook") {
                if (message["method"] === "get") {
                    notebook.set(message["message"]);
                }
            }
        };
    }
};

export async function send_message(channel = "status"
    , message) {
    socket.send(JSON.stringify({
        "channel": channel,
        "message": message
    }));
}