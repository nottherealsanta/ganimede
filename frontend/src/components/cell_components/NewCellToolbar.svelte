<script lang="ts">
  import { Plus } from "lucide-svelte";
</script>

<div class="new-cell-toolbar">
  <div class="line" />
  <div class="add-icon">
    <Plus />
  </div>
</div>

<style>
  .new-cell-toolbar {
    @apply flex 
    w-full h-2
    absolute -top-4 right-0
    items-center justify-center
    bg-transparent
    rounded-md;
    cursor: pointer;
    opacity: 0;
  }
  .new-cell-toolbar:hover {
    opacity: 1;
  }
  .line {
    @apply absolute
    w-full h-[1px]
    bg-gray-400
    rounded-md
    z-0;
  }
  .add-icon {
    @apply flex items-center justify-center
    w-8 h-4 px-2
    bg-gray-50
    rounded-2xl
    z-10;
  }
</style>
