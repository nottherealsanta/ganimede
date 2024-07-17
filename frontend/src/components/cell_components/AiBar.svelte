<script lang="ts">
  import { onMount } from "svelte";
  import { X, SendHorizonal, Ellipsis } from "lucide-svelte";
  import { is_command_mode } from "../../stores/notebook";

  let textarea: HTMLDivElement;
  onMount(() => {
    setTimeout(() => {
      if (textarea) {
        textarea.focus();
        is_command_mode.set(true);
      }
    }, 55);
  });

  export let is_ai_bar_open: boolean;

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Enter") {
      if (e.shiftKey) {
        // Shift + Enter: Insert a line break
        // e.preventDefault();
        e.stopPropagation();
        // document.execCommand("insertLineBreak");
      } else {
        // Enter without Shift: Send AI
        e.preventDefault();
        e.stopPropagation();
        console.log("Sending AI");
        // Implement your send logic here
      }
    }
  }
</script>

<div class="ai-bar">
  <div class="ai-bar-inside">
    <div
      class="textarea"
      contentEditable
      bind:this={textarea}
      on:keydown={handleKeydown}
    ></div>
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
        is_ai_bar_open = false;
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
    ring-2 ring-blue-500/75;
  }
  .textarea {
    @apply w-full p-1 text-sm bg-transparent;
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
