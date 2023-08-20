<script>
  import PrimeButton from "../cell_components/PrimeButton.svelte";
  import DeleteButton from "../cell_components/DeleteButton.svelte";

  import Drag from "../cell_components/Icons/drag.svelte";
  import MenuButton from "../cell_components/MenuButton.svelte";
  import { pc_graph } from "../../stores/_notebook";
  import TissueRunButton from "./TissueRunButton.svelte";

  export let cell;

  export let is_hover = false;
</script>

<div
  class="flex bg-oli dark:bg-oli-800 h-6 w-full rounded-tr p-0.5 border-b border-oli-100 dark:border-oli-600 cursor-grab active:cursor-grabbing"
  on:mousedown
  on:mosueup
>
  {#if cell.type === "code" || cell.id in $pc_graph}
    <TissueRunButton {cell} />
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
