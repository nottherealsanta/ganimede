<script>
  import { flip } from "svelte/animate";
  import { fly } from "svelte/transition";
  import { notifications } from "../../stores/notifications.js";

  export let themes = {
    danger: "#E26D69",
    success: "#84C991",
    warning: "#F9DAA9",
    info: "#ACCBEE",
    default: "#aaaaaa",
  };

  function fade(hex, opacity) {
    let r = parseInt(hex.slice(1, 3), 16);
    let g = parseInt(hex.slice(3, 5), 16);
    let b = parseInt(hex.slice(5, 7), 16);

    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
  }
</script>

<div class="notifications">
  {#each $notifications as notification (notification.id)}
    <div
      animate:flip
      class="toast rounded"
      style="border: 1px solid {themes[
        notification.type
      ]}; background-color: {fade(themes[notification.type], 0.1)};"
    >
      <div class="content py-[5px] px-3">{notification.message}</div>
      {#if notification.icon}<i class={notification.icon} />{/if}
    </div>
  {/each}
</div>

<style>
  .notifications {
    position: fixed;
    top: 30px;
    left: 0;
    right: 0;
    margin: 0 auto;
    padding: 0;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    pointer-events: none;
  }

  .toast {
    flex: 0 0 auto;
    margin-bottom: 5px;
    padding-right: 25px;
  }

  .content {
    display: block;
    font-weight: 500;
    font-family: Inter;
  }
</style>
