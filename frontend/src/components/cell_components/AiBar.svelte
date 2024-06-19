<script lang="ts">
  import { onMount } from "svelte";
  import { X, SendHorizonal, Ellipsis } from "lucide-svelte";

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
    <button class="aibar-button" aria-label="Send AI">
      <SendHorizonal size="14" />
    </button>
    <button class="aibar-button" aria-label="Send AI">
      <Ellipsis size="14" />
    </button>
    <button
      class="aibar-button"
      aria-label="Close AI Bar"
      on:click={() => {
        ai_bar = false;
        console.log(ai_bar);
      }}
    >
      <X size="14" />
    </button>
  </div>
</div>

<style>
  .ai-bar {
    @apply flex
    w-full h-auto min-h-6 px-1 py-1
    items-center justify-center
    bg-gray-100
    overflow-y-auto
    rounded-md
    border-y-2 border-gray-100;
  }
  .ai-bar-inside {
    @apply flex 
    w-full h-full px-1 py-1
    bg-white
    items-center justify-center 
    rounded-md 
    border-2 border-gray-300;
  }
  .textarea {
    @apply w-full min-w-[10rem] p-1 text-sm bg-transparent;
    font-family: "IBM Plex Sans", sans-serif;
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
    text-gray-500;
  }
  .aibar-button:hover {
    @apply bg-gray-100;
  }
</style>
