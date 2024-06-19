<script lang="ts">
  import {
    Book,
    Radius,
    Database,
    Package,
    Sparkles,
    Settings,
  } from "lucide-svelte";
  let show: boolean = false;

  function toggle() {
    show = !show;
  }
</script>

<div class="sidebar-buttons">
  <button class="toggle-button" on:click={toggle}>
    <Book class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={toggle}>
    <Database class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={toggle}>
    <Radius class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={toggle}>
    <Package class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={toggle}>
    <Sparkles class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={toggle}>
    <Settings class="w-4 h-4" />
  </button>
</div>

<div
  class="sidebar"
  style="visibility: {show ? 'visible' : 'hidden'}; 
  display: {show ? 'block' : 'none'}"
>
  Notebooks
  <div class="section"></div>
  Database Connections
  <div class="section"></div>
  Kernel
  <div class="section"></div>
  Environment
  <div class="section"></div>
  AI Copilot
  <div class="section"></div>
  Settings
  <div class="section"></div>
</div>

<style>
  .sidebar-buttons {
    @apply flex flex-col 
    h-full min-w-8 max-w-8 pt-1 
  bg-white border-r-2 border-gray-200;
  }
  .sidebar {
    @apply flex flex-col 
    h-full w-[25%] px-2 pt-4 m-0 
  bg-white border-r-2 border-gray-200 
  text-gray-700;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 600;
  }
  .toggle-button {
    @apply flex 
    w-full h-12 p-0 my-0 
    items-center justify-center 
  bg-white
    rounded 
    text-xs text-gray-500;
  }
  .toggle-button:hover {
    @apply bg-gray-100 text-gray-600;
  }
  .section {
    @apply flex 
    h-fit min-h-24 w-auto pb-2 mb-2 
    bg-transparent 
    border-b-2 border-gray-200;
  }
</style>
