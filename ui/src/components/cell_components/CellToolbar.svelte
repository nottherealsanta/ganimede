<script>
  import PrimeButton from "../cell_components/PrimeButton.svelte";
  import DeleteButton from "../cell_components/DeleteButton.svelte";
  import TurnToTissueButton from "./TurnToTissueButton.svelte";

  import Drag from "../cell_components/Icons/drag.svelte";
  import MenuButton from "../cell_components/MenuButton.svelte";

  import { pc_graph } from "../../stores/_notebook";

  export let cell;

  export let is_hover = false;
</script>

<div
  class="bg-oli dark:bg-oli-800 rounded-t flex h-fit w-full p-0.5 border-b border-oli-100 dark:border-oli-600 cursor-grab active:cursor-grabbing"
  on:mousedown
  on:mouseup
>
  {#if cell.type === "code" || cell.id in $pc_graph}
    <PrimeButton {cell} />
  {:else if is_hover}
    <TurnToTissueButton {cell} />
  {:else}
    <div class="w-5 h-5"></div>
  {/if}
  {#if is_hover}
    <Drag />
    <div class="flex flex-row ml-auto">
      <MenuButton {cell} />
      <DeleteButton {cell} />
    </div>
  {/if}
</div>
