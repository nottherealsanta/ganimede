<script>
  import PrimeButton from "../cell_components/PrimeButton.svelte";
  import DeleteButton from "../cell_components/DeleteButton.svelte";
  import ExecutionCount from "../cell_components/ExecutionCount.svelte";

  import Drag from "../cell_components/Icons/drag.svelte";
  import MenuButton from "../cell_components/MenuButton.svelte";
  import { pc_graph } from "../../stores/_notebook";

  export let cell;

  export let is_hover = false;
</script>

<div
  class="flex bg-oli dark:bg-oli-600 h-6 w-full rounded-tr p-0.5 border-b border-oli-200 dark:border-oli-600 cursor-grab active:cursor-grabbing"
  on:mousedown
  on:mosueup
>
  {#if cell.type === "code" || cell.id in $pc_graph}
    <PrimeButton {cell} />
    <!-- <ExecutionCount {cell} /> -->
  {:else}
    <div class="h-5 w-5" />
  {/if}
  {#if is_hover}
    <Drag />
    <div class="flex flex-row ml-auto">
      <MenuButton {cell} />
      <DeleteButton {cell} />
    </div>
  {/if}
</div>
