<script lang="ts">
  import { onMount, onDestroy } from "svelte";

  export let cell;

  let elapsedTime = 0;
  let intervalId: number | null = null;
  let startTime: number | null = null;

  function formatTime(seconds: number): string {
    if (seconds < 60) {
      return seconds < 10
        ? seconds.toFixed(1) + "s"
        : Math.round(seconds) + "s";
    } else if (seconds < 3600) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.round(seconds % 60);
      return `${minutes}m ${remainingSeconds}s`;
    } else {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const remainingSeconds = Math.round(seconds % 60);
      return `${hours}h ${minutes}m ${remainingSeconds}s`;
    }
  }

  function formatDetailedTime(milliseconds: number): string {
    if (milliseconds < 1000) {
      return milliseconds.toFixed(0) + "ms";
    } else if (milliseconds < 60000) {
      return (milliseconds / 1000).toFixed(2) + "s";
    } else {
      return formatTime(milliseconds / 1000);
    }
  }

  function formatDate(date: Date): string {
    const pad = (num: number) => num.toString().padStart(2, "0");
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
  }

  $: execution_time = cell.execution_time
    ? formatTime(cell.execution_time.end - cell.execution_time.start)
    : null;

  function startTimer() {
    if (intervalId === null) {
      startTime = Date.now();
      intervalId = setInterval(() => {
        elapsedTime = (Date.now() - startTime!) / 1000;
      }, 100);
    }
  }

  function stopTimer() {
    if (intervalId !== null) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }

  $: if (cell.state === "running") {
    startTimer();
  } else {
    stopTimer();
  }

  onMount(() => {
    if (cell.state === "running") {
      startTimer();
    }
  });

  onDestroy(() => {
    stopTimer();
  });

  $: formattedStartTime = execution_time
    ? cell.execution_time.start
      ? formatDate(new Date(cell.execution_time.start * 1000))
      : null
    : null;
</script>

<div class="cell-status-time">
  {#if cell.state === "running"}
    {formatTime(elapsedTime)}
  {:else if execution_time}
    {execution_time}
    <span class="tooltip">{`Last Run: ${formattedStartTime}`} </span>
  {/if}
</div>

<style>
  .cell-status-time {
    @apply flex relative
    h-full w-16
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs
    text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    font-style: normal;
    user-select: none;
  }

  .tooltip {
    @apply absolute 
    w-fit px-2 py-1 
    bg-gray-700 text-gray-100
    rounded-md
    top-8 left-1/2 transform -translate-x-1/2
    text-nowrap text-xs
    z-20;
    transition: opacity 0.1s ease-out;
    opacity: 0;
    overflow: hidden;
  }
  .cell-status-time:hover .tooltip {
    animation: showTooltip 0.5s ease-in-out forwards;
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
