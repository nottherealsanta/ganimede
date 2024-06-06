<script lang="ts">
  import SaveIcon from "../../assets/icons/save.svelte";
  import RunAllIcon from "../../assets/icons/run_nb.svelte";
  import StopIcon from "../../assets/icons/stop.svelte";
  import RestartIcon from "../../assets/icons/restart_nb.svelte";

  let nb_name: string = "Test Notebook";
</script>

<div class="navbar">
  <!-- Notebook Name -->
  <div class="name">{nb_name}</div>

  <div class="flex-grow"></div>

  <!-- Notebook Actions Save, Run All, Stop, Restart -->
  <div class="actions">
    <button class="action-button">
      <SaveIcon />
      <span class="tooltip">Save</span>
    </button>
    <button class="action-button">
      <RunAllIcon />
      <span class="tooltip">Run All</span>
    </button>
    <button class="action-button">
      <StopIcon />
      <span class="tooltip">Stop</span>
    </button>
    <button class="action-button">
      <RestartIcon />
      <span class="tooltip">Restart</span>
    </button>
  </div>
</div>

<style>
  .navbar {
    @apply top-0 left-0 w-full h-10 
    px-2
    flex items-center
    bg-gray-50
    border-b-2 border-gray-200;
  }
  .name {
    @apply text-gray-800;
    font-family: "Inter", sans-serif;
    font-weight: 600;
  }
  .actions {
    @apply flex;
  }
  .action-button {
    @apply relative
    h-8 w-8 
    mx-0.5 p-2
    bg-transparent
    rounded-lg
    text-sm text-gray-800;
  }
  .action-button:hover {
    @apply bg-gray-200;
  }
  .tooltip {
    @apply absolute 
    w-fit px-1 py-0.5 
    bg-gray-700 text-gray-100
    rounded-md
    -bottom-6 right-1/3
    text-nowrap text-xs;
    transition: opacity 0.25s ease-out;
    opacity: 0;
    overflow: hidden;
  }
  .action-button:hover .tooltip {
    animation: showTooltip 1s ease-in-out forwards;
  }

  @keyframes showTooltip {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
</style>
