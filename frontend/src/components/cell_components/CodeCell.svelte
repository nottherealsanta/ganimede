<script lang="ts">
  import CodeEditor from "./CodeEditor.svelte";
  import CodeCellSidebar from "./CodeCellSidebar.svelte";
  import { cell_maps } from "../../scripts/test_nb";

  export let cell_id: string;
  let cell: any = cell_maps[cell_id];
  let code: string = cell.source;
</script>

<div class="code-cell">
  <div class="flex flex-row">
    <CodeCellSidebar {cell_id} />
    <CodeEditor {cell_id} />
  </div>
</div>

<style>
  .code-cell {
    @apply flex flex-col
    w-full h-auto
    m-0
    bg-transparent
    border border-gray-200
    rounded;
  }
</style>
