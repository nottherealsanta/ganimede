<script lang="ts">
  import { EllipsisVertical } from "lucide-svelte";
  import ContextMenu from "./ContextMenu.svelte";
  import { onDestroy } from "svelte";

  export let is_hover: boolean = false;
  export let is_active: boolean = false;

  let is_open = false;
  let menuButtonElement: HTMLButtonElement;
  let dropdownElement: HTMLDivElement;
  let dropdown_y = 0;

  function handleClickOutside(event: MouseEvent) {
    if (
      dropdownElement &&
      !dropdownElement.contains(event.target as Node) &&
      menuButtonElement &&
      !menuButtonElement.contains(event.target as Node)
    ) {
      toggleOpen();
    }
  }

  function toggleOpen() {
    if (is_open) {
      document.removeEventListener("click", handleClickOutside);
      is_open = false;
    } else {
      document.addEventListener("click", handleClickOutside);
      is_open = true;
      // We'll update the position after the dropdown is rendered
      setTimeout(updateDropdownPosition, 0);
    }
  }

  function updateDropdownPosition() {
    if (!menuButtonElement || !dropdownElement) return;

    let menuButton_y = menuButtonElement.getBoundingClientRect().y;
    let dropdown_height = dropdownElement.getBoundingClientRect().height;
    let screen_height = window.innerHeight;

    if (menuButton_y + dropdown_height > screen_height) {
      dropdown_y = -dropdown_height;
    } else {
      dropdown_y = 30;
    }
  }

  onDestroy(() => {
    document.removeEventListener("click", handleClickOutside);
  });
</script>

{#if is_hover || is_open || is_active}
  <div class="relative inline-block text-left dropdown-container">
    <div>
      <button
        class="menu-button"
        on:click|stopPropagation={toggleOpen}
        bind:this={menuButtonElement}
      >
        <EllipsisVertical size="16" />
      </button>
    </div>
    {#if is_open}
      <ContextMenu bind:dropdownElement bind:is_open {dropdown_y} />
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
</style>
