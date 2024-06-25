<script lang="ts">
  import {
    ArrowDown,
    ArrowUp,
    CopyPlus,
    Fullscreen,
    Library,
    MessageSquare,
    Trash2,
  } from "lucide-svelte";

  export let dropdownElement: HTMLDivElement;
  export let is_open: boolean = false;
  export let dropdown_y: number = 0;

  function close_dropdown() {
    is_open = false;
  }

  function format_code() {
    close_dropdown();
    console.log("format code");
  }

  function duplicate_cell() {
    close_dropdown();
    console.log("duplicate cell");
  }

  function move_up() {
    close_dropdown();
    console.log("move up");
  }

  function move_down() {
    close_dropdown();
    console.log("move down");
  }

  function fullscreen() {
    close_dropdown();
    console.log("fullscreen");
  }

  function comment() {
    close_dropdown();
    console.log("comment");
  }

  function delete_cell() {
    close_dropdown();
    console.log("delete cell");
  }
</script>

<div
  class="menu"
  role="menu"
  aria-orientation="vertical"
  aria-labelledby="menu-button"
  tabindex="-1"
  bind:this={dropdownElement}
  style="top: {dropdown_y}px;"
>
  <button class="menu-item" on:click={format_code}>
    <Library size="16" class="mr-2" />
    Format Code
  </button>
  <button class="menu-item" on:click={duplicate_cell}>
    <CopyPlus size="16" class="mr-2" />
    Duplicate Cell
  </button>
  <button class="menu-item" on:click={move_up}>
    <ArrowUp size="16" class="mr-2" />
    Move Up
  </button>
  <button class="menu-item" on:click={move_down}>
    <ArrowDown size="16" class="mr-2" />
    Move Down
  </button>
  <button class="menu-item" on:click={fullscreen}>
    <Fullscreen size="16" class="mr-2" />
    Fullscreen
  </button>
  <button class="menu-item" on:click={comment}>
    <MessageSquare size="16" class="mr-2" />
    Comment
  </button>
  <hr class="my-1" />
  <button class="menu-item text-rose-600" on:click={delete_cell}>
    <Trash2 size="16" class="mr-2" />Delete Cell
  </button>
</div>

<style>
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
