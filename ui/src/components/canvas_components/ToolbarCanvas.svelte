<script>
  import { send_message } from "../../stores/socket";
  import { zoom_in, zoom_out } from "../../stores/zoom.js";
  import { ydoc } from "../../stores/_notebook";

  async function interrupt_kernel() {
    send_message({
      channel: "kernel",
      method: "interrupt",
      message: {},
    });
  }
  async function checkpoint() {
    send_message({
      channel: "notebook",
      method: "checkpoint",
      message: {},
    });
  }

  let kernel_busy = ydoc.getMap("kernel").get("busy");
  ydoc.getMap("kernel").observeDeep(() => {
    kernel_busy = ydoc.getMap("kernel").get("busy");
  });

  let nb_path = ydoc.getText("nb_path");
  ydoc.getText("nb_path").observeDeep(() => {
    nb_path = ydoc.getText("nb_path");
  });

  $: nb_path_show = nb_path.toString().split("/").slice(-1)[0];

  // ---------- SVG
  import Checkpoint from "../../assets/icons/checkpoint.svelte";
  import Interrupt from "../../assets/icons/interrupt.svelte";
  import Restart from "../../assets/icons/restart.svelte";
  import ZoomIn from "../../assets/icons/zoom_in.svelte";
  import ZoomOut from "../../assets/icons/zoom_out.svelte";
</script>

<div
  class=" fixed flex flex-row self-center top-0 align-center items-center w-full h-7 px-2 bg-oli dark:bg-oli-700 border-b border-oli-300 dark:border-oli-500 justify-left align-middle pointer-events-auto fill-oli-400 stroke-oli-400 dark:fill-oli-200 dark:stroke-oli-200"
  style="
    left: 50%;
    transform: translateX(-50%);
    "
>
  <!-- Notebook Path -->
  <div
    class="mx-2 text-[11px] font-['Roboto_Mono'] text-oli-600 dark:text-oli-200"
    title={nb_path}
  >
    /{nb_path_show}
  </div>

  <div class="mx-auto flex flex-row">
    <!-- Kernel Status Indicator -->
    <button
      class="bg-transparent h-6 w-6 mx-1 m-0 p-0 flex align-middle justify-center items-center self-center border-0 {kernel_busy
        ? 'fill-yellow-600'
        : 'fill-green-600'}"
      alt="Status"
      title="kernel status: {kernel_busy ? 'Busy' : 'Idle'}"
    >
      <svg width="20" height="20">
        <circle cx="10" cy="10" r="9" stroke-width="0" opacity="0.10" />
        <circle cx="10" cy="10" r="6.5" stroke-width="0" opacity="0.30" />
        <circle cx="10" cy="10" r="4" stroke-width="0" opacity="1" />
      </svg>
    </button>
    <!-- Checkpoint -->
    <button
      class="bg-transparent h-6 w-6 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
      on:click={checkpoint}
      title="Checkpoint"
    >
      <Checkpoint />
    </button>
    <!-- Interupt -->
    <button
      class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
      on:click={interrupt_kernel}
      title="Interrupt"
    >
      <Interrupt />
    </button>
    <!-- Restart -->
    <button
      class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
      on:click={interrupt_kernel}
      title="Restart"
    >
      <Restart />
    </button>

    <!-- Zoom + -->
    <button
      class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
      on:click={zoom_in}
      title="Zoom In"
    >
      <ZoomIn />
    </button>
    <!-- Zoom - -->
    <button
      class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
      on:click={zoom_out}
      title="Zoom Out"
    >
      <ZoomOut />
    </button>
  </div>
</div>
