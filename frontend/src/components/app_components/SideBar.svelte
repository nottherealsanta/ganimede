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
  import { onMount } from "svelte";

  let show: boolean = false;
  let activeSection: string | null = null;
  let sidebarWidth: number = 300; // Default width
  let isDragging: boolean = false;
  let startX: number;
  let startWidth: number;

  function toggle(section: string) {
    show = activeSection !== section || !show;
    activeSection = show ? section : null;
  }

  function startResize(event: MouseEvent) {
    isDragging = true;
    startX = event.clientX;
    startWidth = sidebarWidth;
    document.addEventListener("mousemove", resize);
    document.addEventListener("mouseup", stopResize);
  }

  function resize(event: MouseEvent) {
    if (isDragging) {
      const diff = event.clientX - startX;
      sidebarWidth = Math.max(200, Math.min(600, startWidth + diff));
    }
  }

  function stopResize() {
    isDragging = false;
    document.removeEventListener("mousemove", resize);
    document.removeEventListener("mouseup", stopResize);
  }

  onMount(() => {
    return () => {
      document.removeEventListener("mousemove", resize);
      document.removeEventListener("mouseup", stopResize);
    };
  });
</script>

<div class="sidebar-container">
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

  <div
    class="sidebar"
    style="width: {show ? sidebarWidth + 'px' : '0px'}; visibility: {show
      ? 'visible'
      : 'hidden'};
      display: {show ? 'block' : 'none'}"
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

    {#if show}
      <div class="resize-handle" on:mousedown={startResize}></div>
    {/if}
  </div>
</div>

<style>
  .sidebar-container {
    @apply flex h-full;
  }

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
    position: relative;
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

  .resize-handle {
    @apply absolute top-0 right-0 w-0.5 h-full cursor-ew-resize bg-gray-50;
    transition: width 0.2s;
  }

  .resize-handle:hover {
    @apply w-1 bg-gray-200;
  }
</style>
