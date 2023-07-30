<script>
  export let cell;

  function connector_click(e) {
    e.preventDefault();
    console.log("button click");
    console.log(e.target.id);
    e.stopPropagation();
  }

  let is_hover = false;

  // Components
  import ToolbarSlot from "./ToolbarSlot.svelte";
  import Connector from "../Icons/connector.svelte";
  import Python from "../Icons/python.svelte";
  import Markdown from "../Icons/markdown.svelte";
  import Disconnect from "../Icons/disconnect.svelte";
  import NewCellMenu from "../Icons/newCellMenu.svelte";
  import { create_cell } from "../../../stores/_notebook.js";

  async function new_code_cell(e) {
    // e.stopPropagation();
    // e.preventDefault();
    // console.log("new code cell", e);
    // // sendMessage("new_code_cell", "code");
    create_cell("code");
  }

  async function new_markdown_cell() {
    // sendMessage("new_markdown_cell", "markdown");
    console.log("new markdown cell", cell.id);
  }

  // mouse loc
  // import mouse_pos from "../../../stores/mouse.js";

  // let hover_pos = null;
  // $: if (is_hover && hover_pos === null) {
  //   hover_pos = $mouse_pos.x - cell.left;
  // }
  // $: if (!is_hover) {
  //   hover_pos = null;
  // }
</script>

<div
  class="newcelltoolbar absolute -bottom-[21px] w-fit h-5 bg-transparent"
  on:mouseenter={() => {
    is_hover = true;
  }}
  on:mouseleave={() => {
    is_hover = false;
  }}
  style={is_hover ? "" : "justify-content: center;"}
>
  <!-- <div
    class="absolute bg-sky-700 w-full bottom-[2px] rounded-full"
    style="{is_hover ? 'height: 2px;' : 'height: 0px;'} + "
  /> -->
  {#if is_hover}
    <div
      class="absolute w-fit h-[19px] z-auto -top-[10px] flex flex-row cursor-default bg-oli dark:bg-oli-700 rounded border border-oli-500 dark:border-oli-300 overflow-clip fill-oli-500 dark:fill-gray-300 stroke-oli-500 dark:stroke-oli-400 stroke"
      on:mousedown|stopPropagation={() => {}}
    >
      <!-- <ToolbarSlot><Disconnect /></ToolbarSlot> -->
      <ToolbarSlot on:click={new_code_cell}><Python /></ToolbarSlot>
      <ToolbarSlot><Connector /></ToolbarSlot>
      <ToolbarSlot on:click={new_markdown_cell}><Markdown /></ToolbarSlot>
      <!-- <ToolbarSlot><NewCellMenu /></ToolbarSlot> -->
    </div>
  {:else}
    <div
      class="absolute w-3 h-5 -top-[10px] ml-[25px] rounded-full flex items-center justify-center bg-transparent cursor-pointer stroke-oli-500 dark:stroke-oli-200 stroke-2 fill-oli-50 dark:fill-oli-500"
      id="new-cell-toolbar"
      on:click|stopPropagation={connector_click}
      on:keydown={() => {}}
    >
      <Connector />
    </div>
  {/if}
</div>
