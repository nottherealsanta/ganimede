<script>
  import { Trash2 } from "lucide-svelte";
  import HeadingCollapsible from "./bar_components/HeadingCollapsible.svelte";
  export let cell;
  export let is_hover;

  import { active_cell_id, n_descendants } from "../../stores/notebook";

  $: is_active = $active_cell_id === cell.id;
  $: is_markdown = cell.type === "markdown";
  $: is_heading = is_markdown && cell.source.toJSON().startsWith("#");
</script>

{#if $n_descendants[cell.id] > 0}
  <div class="left-controls">
    <HeadingCollapsible {cell} show={is_hover || is_active} />
  </div>
{/if}

<style>
  .left-controls {
    @apply absolute flex 
    w-6 h-6 p-1
    top-1 -left-7
    items-center justify-center
    bg-transparent
    z-10;
  }
</style>
