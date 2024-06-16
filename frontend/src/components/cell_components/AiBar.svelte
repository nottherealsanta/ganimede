<script lang="ts">
  import { onMount } from "svelte";
  import { X } from "lucide-svelte";

  // on Mount focus the textarea
  let textarea: HTMLDivElement;
  onMount(() => {
    textarea.focus();
  });

  export let ai_bar: boolean;
</script>

<div class="ai-bar">
  <div class="ai-bar-inside">
    <div class="textarea" contentEditable bind:this={textarea}></div>
    <div class="flex-grow"></div>
    <!-- <button
      class="aibar-button"
      aria-label="Close AI Bar"
      on:click={() => {
        ai_bar = false;
        console.log(ai_bar);
      }}
    >
      <X size="14" />
    </button> -->
  </div>
</div>

<style>
  .ai-bar {
    @apply flex
    w-full h-auto min-h-6
    py-0.5 px-0.5
    items-center justify-center
    bg-gray-50
    overflow-y-auto
    border-y-2 border-gray-100;
  }
  .ai-bar-inside {
    @apply flex 
    w-full h-full px-2 py-1
    bg-white
    items-center justify-center 
    rounded-md 
    border-2 border-gray-100;
  }
  .textarea {
    @apply min-w-[10rem] py-1 text-sm;
    font-family: "Inter", sans-serif;
  }
  .textarea:focus {
    @apply outline-none;
  }
  .textarea:empty:before {
    content: "Ask AI";
    color: #a0aec0;
  }
  .aibar-button {
    @apply flex
    h-8 w-8
    px-2 py-1 
    items-center justify-center
    bg-white
    rounded-md
    cursor-pointer
    text-sm
    text-gray-400;
    font-family: "Inter", sans-serif;
    font-weight: 500;
  }
  .aibar-button:hover {
    @apply bg-gray-100;
  }
</style>
