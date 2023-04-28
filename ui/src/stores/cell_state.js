// export const CellStates = {
//     Idle: "idle",
//     Queued: "queued",
//     Running: "running",
//     Done: "done",
// };

// import { cells } from "./notebook.js"
// import { derived } from "svelte/store";

// // export let cell_ids = derived(cells, $cells => {
// //     return $cells.map(c => c.id);
// // }
// // );

// // create a derived store that is map of cell_ids to cell_states

// export let cell_states = derived(cells, $cells => {
//     let cell_states = {};
//     $cells.forEach(c => {
//         // cell_states[c.id] = c.state;
//         if(c.state){
//             cell_states[c.id] = c.state;
//         } else {
//             cell_states[c.id] = CellStates.Idle;
//         }
//     });
//     return cell_states;
// }
// );