<script lang="ts">
  import { ChevronDown, ChevronRight } from "lucide-svelte";

  export let is_collapsed: boolean = false;
</script>

<button
  class="collapsible-chevron"
  on:click={() => (is_collapsed = !is_collapsed)}
  type="button"
>
  <div class="collapse-text">Collapse</div>
</button>

<style>
  .collapsible-chevron {
    @apply flex absolute
    w-1
    -left-0
    bg-transparent
    items-center justify-center
    cursor-pointer z-10
    rounded-r-3xl
    ease-in-out transition-all duration-200;
    height: calc(100% - 6px);
    top: 3px;
  }
  .collapsible-chevron:hover {
    @apply w-[6px] bg-sky-500;
    height: calc(100% - 6px);
    top: 3px;
  }

  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    80% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  .collapse-text {
    @apply absolute mr-6 hidden text-xs text-gray-600;
    transform: rotate(-90deg);
    animation: fadeIn 2s ease-in-out;
  }

  .collapsible-chevron:hover .collapse-text {
    @apply block;
  }
</style>
