<script>
  export let cell;

  import { ypc_graph } from "../../stores/_notebook";
  import * as Y from "yjs";

  let div = null;
  // run
  async function button_click() {
    let parent_array = new Y.Array();
    ypc_graph.set(cell.id, parent_array);
  }
</script>

<div
  class="flex flex-none bg-transparent hover:bg-oli-100 dark:hover:bg-oli-800 active:bg-oli-200 dark:active:bg-oli-700 w-5 h-5 p-0 m-0 rounded-sm items-center justify-center stroke-black dark:stroke-white fill-black dark:fill-white cursor-pointer pointer-events-auto"
  on:mousedown|stopPropagation={(e) => {
    button_click();
  }}
  bind:this={div}
>
  T
</div>
