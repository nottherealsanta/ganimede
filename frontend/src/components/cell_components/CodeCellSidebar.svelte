<script lang="ts">
  import { Play } from "lucide-svelte";

  export let cell_id: string;
</script>

<div class="cell-sidebar">
  <Play size="16" />
</div>

<style>
  .cell-sidebar {
    @apply flex 
    w-8 h-full
    pt-[9px]
    justify-center
    bg-gray-50
    rounded-l
    text-gray-600;
  }
</style>
