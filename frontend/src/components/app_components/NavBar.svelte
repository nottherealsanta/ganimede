<script lang="ts">
  import { Bookmark, SkipForward, Square, RotateCcw } from "lucide-svelte";

  let nb_name: string = "Test Notebook";
</script>

<div class="navbar">
  <!-- Notebook Name -->
  <div class="name">{nb_name}</div>

  <div class="flex-grow"></div>

  <!-- Notebook Actions Save, Run All, Stop, Restart -->
  <div class="actions">
    <button class="action-button">
      <Bookmark />
      <span class="tooltip">Save</span>
    </button>
    <button class="action-button">
      <SkipForward />
      <span class="tooltip">Run All</span>
    </button>
    <button class="action-button">
      <Square />
      <span class="tooltip">Stop</span>
    </button>
    <button class="action-button">
      <RotateCcw />
      <span class="tooltip">Restart</span>
    </button>
  </div>
</div>

<style>
  .navbar {
    @apply flex
    top-0 left-0 w-full h-10 
    px-2
    items-center
    bg-gray-50
    border-b-2 border-gray-200;
  }
  .name {
    @apply text-gray-800;
    font-family: "Inter", sans-serif;
    font-weight: 600;
  }
  .actions {
    @apply flex;
  }
  .action-button {
    @apply relative flex
    h-8 w-8 p-2
    items-center justify-center
    bg-transparent
    rounded-lg
    text-sm text-gray-600;
  }
  .action-button:hover {
    @apply bg-gray-100;
  }
  .tooltip {
    @apply absolute 
    w-fit px-1 py-0.5 
    bg-gray-700 text-gray-100
    rounded-md
    -bottom-6 right-1/3
    text-nowrap text-xs;
    transition: opacity 0.25s ease-out;
    opacity: 0;
    overflow: hidden;
  }
  .action-button:hover .tooltip {
    animation: showTooltip 1s ease-in-out forwards;
  }

  @keyframes showTooltip {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
</style>
