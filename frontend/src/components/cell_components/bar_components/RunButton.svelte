<script lang="ts">
  import { LoaderCircle, Play, Square } from "lucide-svelte";

  export let cell: any;
  $: exe_count_test =
    cell.execution_count === undefined ? " " : cell.execution_count.toString();

  // idle -> queued -> running -> idle

  import { queue_cell } from "../../../stores/notebook";

  async function run_cell() {
    if (cell.state === "idle") {
      queue_cell(cell.id);
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
  <button
    class="flex flex-row items-center justify-center"
    on:click={run_cell}
    disabled={cell.state !== "idle"}
  >
    {#if cell.state === "idle"}
      <Play
        size="14"
        strokeWidth="2"
        class="fill-none group-hover:fill-current mx-0.5"
      />
    {:else if cell.state === "queued"}
      <div class="queue">
        <LoaderCircle size="14" strokeWidth="2" />
      </div>
    {:else if cell.state === "running"}
      <div class="running">
        <LoaderCircle size="14" strokeWidth="2" />
      </div>
    {/if}
    {#if is_local_hover && cell.state !== "idle"}
      <span class="ml-1">
        {#if cell.state === "queued"}
          Queued
        {:else if cell.state === "running"}
          Running
        {/if}
      </span>
    {/if}
  </button>
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
  }

  .run-button:hover {
    @apply bg-gray-100 text-gray-400;
  }
  .run-button:active {
    @apply bg-gray-200 text-gray-600;
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
