import { derived, writable } from "svelte/store";
import { get } from 'svelte/store'
import * as Y from "yjs";
import { WebsocketProvider } from "y-websocket";

const doc = new Y.Doc();

const websocket_provider = new WebsocketProvider(
    "ws://localhost:1234",
    "g-y-room",
    doc
);

websocket_provider.on("status", event => {
    console.log("yjs status: ", event.status); // logs "connected" or "disconnected"
});



export const xells = doc.getMap("cells");


xells.observe((event) => {
    console.log("cells changed", event, xells.toJSON());
});

let new_cell = new Y.Map();
new_cell.set('id', 'X-ewnmf8')
new_cell.set('type', 'code')

let code = new Y.Text();
code.insert(0, 'print("hello world")')
new_cell.set('content', code)

new_cell.set('language', 'python')
new_cell.set('output', 'hello world')

xells.set("X-ewnmf8", new_cell);

console.log("-", xells);
console.log(">", xells["X-ewnmf8"]);
console.log(">>", xells.get("X-ewnmf8"));
let x = xells.get("X-ewnmf8");
console.log(">>>", x.toJSON());
console.log(">>>>", xells.get("X-ewnmf8").get("content"));
