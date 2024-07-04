// import type * as Party from "partykit/server";

// export default class Server implements Party.Server {
//   constructor(readonly room: Party.Room) {}

//   onConnect(conn: Party.Connection, ctx: Party.ConnectionContext) {
//     // A websocket just connected!
//     console.log(
//       `Connected:
//   id: ${conn.id}
//   room: ${this.room.id}
//   url: ${new URL(ctx.request.url).pathname}`
//     );

//     // let's send a message to the connection
//     conn.send("hello from server");
//   }

//   onMessage(message: string, sender: Party.Connection) {
//     // let's log the message
//     console.log(`connection ${sender.id} sent message: ${message}`);
//     // as well as broadcast it to all the other connections in the room...
//     this.room.broadcast(
//       `${sender.id}: ${message}`,
//       // ...except for the connection it came from
//       [sender.id]
//     );
//   }
// }

// Server satisfies Party.Worker;

import type * as Party from "partykit/server";
import { onConnect } from "y-partykit";

export default class YjsServer implements Party.Server {
  constructor(public room: Party.Room) {}
  static async onBeforeConnect(request: Party.Request, lobby: Party.Lobby) { 
    console.log("onBeforeConnect request: ", request);
    console.log("onBeforeConnect lobby: ", lobby);
    return true; 
  }
  onConnect(conn: Party.Connection) {
    return onConnect(conn, this.room, {
      callback: {
        async handler(yDoc) {
          // console.log("Yjs document updated: ", yDoc.toJSON());
          // const cells = yDoc.getArray("cells").toJSON();
          // console.log("cells: ", cells, cells.length);

          // for (let i = 0; i < cells.length; i++) {
          //   console.log("cell: ", cells[i]);
          //   console.log("cell map: ", yDoc.getMap(cells[i]).toJSON());
          // }
        },
        // control how often handler is called with these options
        debounceWait: 2000, // default: 2000 ms
        debounceMaxWait: 20000, // default: 10000 ms
        timeout: 5000 // default: 5000 ms
      }
    });
  }
  // onMessage(message: string, sender: Party.Connection) {
  //   console.log(`connection ${sender.id} sent message: ${message}`);
  //   this.room.broadcast(
  //     `${sender.id}: ${message}`,
  //     [sender.id]
  //   );
  // }
}