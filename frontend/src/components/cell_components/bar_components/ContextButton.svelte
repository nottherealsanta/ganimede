<script lang="ts">
  import {
    ArrowDown,
    ArrowUp,
    CopyPlus,
    EllipsisVertical,
    Fullscreen,
    Library,
    MessageSquare,
    Trash2,
  } from "lucide-svelte";
  import { onMount, onDestroy } from "svelte";

  export let is_hover: boolean = false;
  export let is_active: boolean = false;

  let is_open = false;

  function handleClickOutside(event: MouseEvent) {
    const dropdown = document.querySelector(".dropdown-container");
    if (dropdown && !dropdown.contains(event.target as Node)) {
      is_open = false;
    }
  }

  function toggleOpen() {
    if (is_open) {
      document.removeEventListener("click", handleClickOutside);
      is_open = false;
    } else {
      document.addEventListener("click", handleClickOutside);
      is_open = true;
    }
  }

  onDestroy(() => {
    document.removeEventListener("click", handleClickOutside);
  });
</script>

{#if is_hover || is_open || is_active}
  <div class="relative inline-block text-left dropdown-container">
    <div>
      <button class="menu-button" on:click={toggleOpen}>
        <EllipsisVertical size="16" />
      </button>
    </div>

    {#if is_open}
      <div
        class="menu"
        role="menu"
        aria-orientation="vertical"
        aria-labelledby="menu-button"
        tabindex="-1"
      >
        <button class="menu-item">
          <Library size="16" class="mr-2" />
          Format Code
        </button>
        <button class="menu-item">
          <CopyPlus size="16" class="mr-2" />
          Duplicate Cell
        </button>
        <button class="menu-item">
          <ArrowUp size="16" class="mr-2" />
          Move Up
        </button>
        <button class="menu-item">
          <ArrowDown size="16" class="mr-2" />
          Move Down
        </button>
        <button class="menu-item">
          <Fullscreen size="16" class="mr-2" />
          Fullscreen
        </button>
        <button class="menu-item">
          <MessageSquare size="16" class="mr-2" />
          Comment
        </button>
        <hr class="my-1" />
        <button class="menu-item text-rose-600">
          <Trash2 size="16" class="mr-2" />Delete Cell
        </button>
      </div>
    {/if}
  </div>
{/if}

<style>
  .menu-button {
    @apply relative flex 
    h-7 w-7 p-1 ml-1
    items-center justify-center
    bg-transparent
    rounded-md
    text-gray-500;
  }
  .menu-button:hover {
    @apply bg-gray-100;
  }
  .menu-button:active {
    @apply bg-gray-200 text-gray-800;
  }
  .menu {
    @apply absolute 
    right-0 mt-0 py-1 px-1 w-52
    origin-top-right 
    rounded bg-white 
    text-gray-600
    shadow
    ring-1 ring-gray-200
    z-20;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 400;
  }
  .menu-item {
    @apply flex flex-row rounded 
    w-full px-2 py-2 
    items-center justify-start
    text-left text-sm 
  cursor-pointer;
  }
  .menu-item:hover {
    @apply bg-gray-100;
  }
  .menu-item:active {
    @apply bg-gray-200;
  }
</style>
