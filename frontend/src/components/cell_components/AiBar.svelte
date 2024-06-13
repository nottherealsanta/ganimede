<script lang="ts">
  import { Sparkles } from "lucide-svelte";
</script>

<div class="ai-bar">
  <textarea class="textarea" placeholder="AI Copilot"></textarea>
  <div class="flex-grow"></div>
  <button class="aibar-button" aria-label="Run AI Copilot">
    <Sparkles size="14" class="mx-2" />Generate
  </button>
</div>

<style>
  .ai-bar {
    @apply flex
    w-full h-auto min-h-8
    py-2 px-2
    items-center justify-center
    bg-white
    overflow-y-auto
    border-y-2 border-gray-100;
  }
  .textarea {
    @apply w-fit h-8
    px-2
    bg-red-400
    border-none
    resize-none
    outline-none
    text-gray-700
    text-base;
    font-family: "Inter", sans-serif;
  }
  .aibar-button {
    @apply flex
    h-full w-fit
    px-2 py-1 
    items-center justify-center
    bg-white
    rounded-md
    border-2 border-fuchsia-200
    cursor-pointer
    text-sm
    text-gray-600;
    font-family: "Inter", sans-serif;
    font-weight: 500;
  }
</style>
