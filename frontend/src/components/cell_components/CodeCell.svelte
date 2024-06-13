<script lang="ts">
  import CodeEditor from "./CodeEditor.svelte";
  import CodeCellBar from "./CodeCellBar.svelte";
  import { cell_maps } from "../../scripts/test_nb";

  export let cell_id: string;
  export let is_hover: boolean = false;
  let cell: any = cell_maps[cell_id];
  let code: string = cell.source;
</script>

<div class="code-cell">
  <div class="flex flex-col">
    <CodeCellBar {cell_id} {is_hover} />
    <CodeEditor {cell} />
  </div>
</div>

<style>
  .code-cell {
    @apply flex flex-col
    w-full h-auto
    m-0
    bg-transparent
    border-2 border-gray-100
    rounded-md;
  }
</style>
