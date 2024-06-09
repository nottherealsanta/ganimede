<script lang="ts">
  import { Plus } from "lucide-svelte";
</script>

<div class="new-cell-toolbar">
  <div class="line" />
  <div class="add-icon">
    <Plus size="12" />
  </div>
</div>

<style>
  .new-cell-toolbar {
    @apply flex 
    w-full h-2 absolute -top-[15px] right-0 
    items-center justify-center 
    bg-transparent 
    rounded-full;
    cursor: pointer;
    opacity: 0;
  }
  .new-cell-toolbar:hover {
    opacity: 1;
    @apply bg-gray-100;
  }
  .line {
    @apply absolute w-full h-[1px] bg-gray-300 rounded-md z-0;
  }
  .add-icon {
    @apply flex 
    w-8 h-2 px-2 
    items-center justify-center 
    bg-gray-100 
    rounded-2xl 
    z-10;
  }
</style>
