<script lang="ts">
  import CodeEditor from "./CodeEditor.svelte";
  import { cell_maps } from "../../scripts/test_nb";
  import Output from "./outputs/Output.svelte";
  import CellBar from "./CellBar.svelte";

  export let cell: any;
  export let is_hover: boolean = false;
  // let cell: any = cell_maps[cell_id];

  import { active_cell_id, is_command_mode } from "../../stores/notebook.js";
</script>

<CellBar {cell} {is_hover} />

<div
  class="code-cell"
  on:click={(e) => {
    active_cell_id.set(cell.id);
    $is_command_mode = false;
  }}
  role="presentation"
>
  <CodeEditor {cell} {is_hover} />

  {#if cell.outputs && cell.outputs.length > 0}
    <Output {cell} {is_hover} />
  {/if}
</div>

<style>
  .code-cell {
    @apply flex flex-col
    w-full h-auto
    m-0 
    bg-transparent
    rounded-b-md;
  }
</style>
