<script lang="ts">
  import { LoaderCircle, Play, Square } from "lucide-svelte";

  export let cell: any;

  // idle -> queued -> running -> idle

  import { queue_cell, interrupt } from "../../../stores/notebook";

  async function run_cell() {
    if (cell.state === "idle") {
      queue_cell(cell.id);
    } else {
      console.log("interrupting cell");
      interrupt();
    }
  }

  // local hover
  let is_local_hover = false;
</script>

<div
  class="run-button group"
  on:mouseenter={() => {
    is_local_hover = true;
  }}
  on:mouseleave={() => {
    is_local_hover = false;
  }}
>
  <button class="flex flex-row items-center justify-center" on:click={run_cell}>
    {#if cell.state === "idle"}
      <Play
        size="14"
        strokeWidth="2"
        class="fill-none group-hover:fill-current mx-0.5"
      />
    {:else if cell.state !== "idle" && is_local_hover}
      <Square size="14" strokeWidth="2" class="text-gray-600 mx-0.5" />
    {/if}
    {#if cell.state === "queued" && !is_local_hover}
      <div class="queue">
        <LoaderCircle size="14" strokeWidth="2" class="mx-0.5" />
      </div>
    {:else if cell.state === "running" && !is_local_hover}
      <div class="running">
        <LoaderCircle size="14" strokeWidth="2" class="mx-0.5" />
      </div>
    {/if}
  </button>
</div>

<div class="status">
  {#if cell.state === "queued"}
    <span class="ml-1"> Queued </span>
  {:else if cell.state === "running"}
    <span class="ml-1"> Running </span>
  {/if}
</div>

<style>
  .run-button {
    @apply flex 
    h-7 w-fit
    px-1 ml-1
    items-center justify-center
    bg-transparent
    rounded
    border border-transparent
    cursor-pointer
    text-xs
    text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
    transition: all 0.2s;
  }

  .run-button:hover {
    @apply bg-gray-100 text-gray-400;
  }
  .run-button:active {
    @apply bg-gray-200 text-gray-600;
  }

  .status {
    @apply text-xs text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
  }

  .queue {
    @apply w-fit h-fit;
    animation: queue_spin 2s linear infinite;
  }

  .running {
    @apply w-fit h-fit;
    animation: run_spin 1s linear infinite;
  }

  @keyframes queue_spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(-360deg);
    }
  }

  @keyframes run_spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
