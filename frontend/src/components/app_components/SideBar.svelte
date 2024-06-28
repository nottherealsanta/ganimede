<script lang="ts">
  import {
    Book,
    Radius,
    Users,
    Package,
    Sparkles,
    Settings,
  } from "lucide-svelte";
  import NotebookSection from "./sidebar_components/NotebookSection.svelte";
  let show: boolean = false;
  let activeSection: string | null = null;

  function toggle(section: string) {
    show = activeSection !== section || !show;
    activeSection = show ? section : null;
  }
  // TODO: Add Database and Environment sections
</script>

<div class="sidebar-buttons">
  <button class="toggle-button" on:click={() => toggle("notebooks")}>
    <Book class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={() => toggle("live-share")}>
    <Users class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={() => toggle("kernel")}>
    <Radius class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={() => toggle("ai-copilot")}>
    <Sparkles class="w-4 h-4" />
  </button>
  <button class="toggle-button" on:click={() => toggle("settings")}>
    <Settings class="w-4 h-4" />
  </button>
</div>

<!-- style="visibility: {show ? 'visible' : 'hidden'}; 
display: {show ? 'block' : 'none'}" -->
<div
  class="sidebar"
  style="width: {show ? '25%' : '0px'}; visibility: {show
    ? 'visible'
    : 'hidden'};"
>
  {#if activeSection === "notebooks"}
    <NotebookSection />
  {/if}
  {#if activeSection === "live-share"}
    <div class="section">Live Share</div>
  {/if}
  {#if activeSection === "kernel"}
    <div class="section">Kernel</div>
  {/if}
  {#if activeSection === "ai-copilot"}
    <div class="section">AI Copilot</div>
  {/if}
  {#if activeSection === "settings"}
    <div class="section">Settings</div>
  {/if}
</div>

<style>
  .sidebar-buttons {
    @apply flex flex-col 
    h-full min-w-8 max-w-8 pt-1 
  bg-white border-r-2 border-gray-200;
  }
  .sidebar {
    @apply flex flex-col 
    h-full px-2 pt-4 m-0 
  bg-white border-r-2 border-gray-200 
  text-gray-700;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 600;
    /* transition: width 0.1s; */
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
