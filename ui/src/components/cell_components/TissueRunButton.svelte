<script>
  export let cell;

  let hover = false;
  let execution_count;
  $: if (cell) {
    if (cell.execution_count === null) {
      execution_count = "[ ]";
    } else {
      execution_count = cell.execution_count;
    }
  }

  let div = null;
  // run
  import { send_message } from "../../stores/socket";
  import { ypc_graph, ydoc } from "../../stores/_notebook";
  async function primary_button_click() {
    queueChildren(cell.id);
  }

  function queueChildren(parent_id) {
    const children = ypc_graph.get(parent_id);
    if (children) {
      children.toJSON().forEach((child_id) => {
        const childCell = ydoc.getMap(child_id).toJSON();
        if (childCell.type === "code") {
          send_message({
            channel: "notebook",
            method: "queue_cell",
            message: {
              cell_id: child_id,
            },
          });
        }
        queueChildren(child_id);
      });
    }
  }
</script>

<div
  class="w-8 h-5 p-0 m-0 flex flex-none bg-transparent hover:bg-oli-100 dark:hover:bg-oli-800 active:bg-oli-200 dark:active:bg-oli-700 rounded items-center justify-center stroke-black dark:stroke-white fill-black dark:fill-white cursor-pointer pointer-events-auto"
  on:mousedown|stopPropagation={(e) => {
    primary_button_click();
  }}
  on:keydown={() => {}}
  on:mouseenter={() => {
    hover = true;
  }}
  on:mouseleave={() => {
    hover = false;
  }}
  bind:this={div}
>
  <svg
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    ><g>
      <path
        d="M12 10.2L5 6L5 18L12 13.8M12 6L12 18L21 12L12 6Z"
        stroke-width="1.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></path>
    </g></svg
  >
</div>
