<script lang="ts">
  import CodeEditor from "./CodeEditor.svelte";
  import CodeCellBar from "./CodeCellBar.svelte";
  import { cell_maps } from "../../scripts/test_nb";
  import Output from "./outputs/Output.svelte";

  export let cell_id: string;
  export let is_hover: boolean = false;
  let cell: any = cell_maps[cell_id];
  let code: string = cell.source;
</script>

<div class="code-cell">
  <CodeCellBar {cell_id} {is_hover} />
  <CodeEditor {cell} {is_hover} />

  {#if cell.outputs && cell.outputs.length > 0}
    <Output {cell} {is_hover} />
  {/if}
</div>

<style>
  .code-cell {
    @apply flex flex-col
    w-full h-auto
    m-0 z-10
    bg-transparent
    border-2 border-gray-100
    rounded-md;
  }
  .code-cell:hover {
    @apply border-gray-200;
  }
</style>
