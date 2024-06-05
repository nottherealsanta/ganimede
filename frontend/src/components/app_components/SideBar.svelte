<script lang="ts">
  import CloseIcon from "../../assets/icons/close.svelte";
  import MenuIcon from "../../assets/icons/menu.svelte";
  let show: boolean = false;

  function toggle() {
    show = !show;
  }
</script>

<div class="sidebar {show ? 'w-[25rem]' : 'w-8'}">
  <button class="toggle-button" on:click={toggle}>
    {#if show}
      <CloseIcon />
    {:else}
      <MenuIcon />
    {/if}
  </button>
</div>

<style>
  .sidebar {
    @apply relative flex
    h-full min-w-8
    bg-gray-50
    border-r-2 border-gray-200;
    transition: width 0.25s;
  }
  .toggle-button {
    @apply absolute
    w-10 h-10 p-2.5 
    -right-5 top-2
    bg-gray-50 
    rounded-full
    border-2 border-gray-200 
    text-xs text-gray-500;
  }
</style>
