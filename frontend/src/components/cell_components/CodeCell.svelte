<script lang="ts">
  import CodeEditor from "./CodeEditor.svelte";
  import { cell_maps } from "../../scripts/test_nb";
  import Output from "./outputs/Output.svelte";

  export let cell_id: string;
  export let is_hover: boolean = false;
  let cell: any = cell_maps[cell_id];
</script>

<div class="code-cell">
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
    rounded-b-md;
  }
</style>
