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

  let kernel_busy = ydoc.getMap("kernel").get("busy");
  ydoc.getMap("kernel").observeDeep(() => {
    kernel_busy = ydoc.getMap("kernel").get("busy");
  });

  let nb_path = ydoc.getText("nb_path");
  ydoc.getText("nb_path").observeDeep(() => {
    nb_path = ydoc.getText("nb_path");
  });

  $: console.log("nb_path: ", nb_path);
  $: console.log("typeof nb_path: ", typeof nb_path);
  $: nb_path_show = nb_path.toString().split("/").slice(-1)[0];
</script>

<div
  class=" fixed flex flex-row self-center top-[10px] align-center items-center w-[400px] h-6 pl-2 bg-oli dark:bg-oli-700 rounded-full border border-oli-300 dark:border-oli-400 justify-left align-middle pointer-events-auto fill-oli-400 stroke-oli-400 dark:fill-oli-200 dark:stroke-oli-200"
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
    {nb_path_show}
  </div>

  <!-- Save -->
  <button
    class="bg-transparent h-6 w-6 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
    on:click={interrupt_kernel}
    alt="Save"
  >
    <svg
      width="13"
      height="13"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
      ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
        id="SVGRepo_tracerCarrier"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></g><g id="SVGRepo_iconCarrier">
        <path
          d="M5 6.2C5 5.07989 5 4.51984 5.21799 4.09202C5.40973 3.71569 5.71569 3.40973 6.09202 3.21799C6.51984 3 7.07989 3 8.2 3H15.8C16.9201 3 17.4802 3 17.908 3.21799C18.2843 3.40973 18.5903 3.71569 18.782 4.09202C19 4.51984 19 5.07989 19 6.2V21L12 16L5 21V6.2Z"
          stroke-width="2"
          stroke-linejoin="round"
        ></path>
      </g></svg
    >
  </button>
  <!-- Interupt -->
  <button
    class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
    on:click={interrupt_kernel}
    alt="Interrupt Kernel"
  >
    <svg width="9" height="9">
      <rect width="10" height="10" rx="3" />
    </svg>
  </button>
  <!-- Restart -->
  <button
    class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
    on:click={interrupt_kernel}
    alt="Restart"
  >
    <svg
      width="13"
      height="13"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
        id="SVGRepo_tracerCarrier"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></g><g id="SVGRepo_iconCarrier">
        <path
          d="M21 10C21 10 18.995 7.26822 17.3662 5.63824C15.7373 4.00827 13.4864 3 11 3C6.02944 3 2 7.02944 2 12C2 16.9706 6.02944 21 11 21C15.1031 21 18.5649 18.2543 19.6482 14.5M21 10V4M21 10H15"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
        ></path>
      </g></svg
    >
  </button>
  <!-- Kernel Status Indicator -->
  <button
    class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center border-0 {kernel_busy
      ? 'fill-yellow-600'
      : 'fill-green-600'}"
    alt="Status"
  >
    <svg width="20" height="20">
      <circle cx="10" cy="10" r="9" stroke-width="0" opacity="0.10" />
      <circle cx="10" cy="10" r="6.5" stroke-width="0" opacity="0.30" />
      <circle cx="10" cy="10" r="4" stroke-width="0" opacity="1" />
    </svg>
  </button>
  <!-- Zoom + -->
  <button
    class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
    on:click={zoom_in}
    alt="Zoom In"
  >
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
        id="SVGRepo_tracerCarrier"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></g><g id="SVGRepo_iconCarrier">
        <path
          d="M6 12H18M12 6V18"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          data-darkreader-inline-stroke=""
          style="--darkreader-inline-stroke: #e8e6e3;"
        ></path>
      </g></svg
    >
  </button>
  <!-- Zoom - -->
  <button
    class="bg-transparent h-6 w-6 ml-1 m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-50/90 dark:hover:bg-oli-800/90 active:bg-blue-300 rounded border-0"
    on:click={zoom_out}
    alt="Zoom Out"
  >
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
        id="SVGRepo_tracerCarrier"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></g><g id="SVGRepo_iconCarrier">
        <path
          d="M6 12L18 12"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          data-darkreader-inline-stroke=""
          style="--darkreader-inline-stroke: #e8e6e3;"
        ></path>
      </g></svg
    >
  </button>
</div>
