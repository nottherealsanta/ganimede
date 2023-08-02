<script>
  import Outputs from "./cell_components/Outputs.svelte";

  export let cell;

  import CodeEditor from "./cell_components/CodeEditor.svelte";
  let focus;

  let is_hover = false;

  function toggle_input_collapsed(e) {
    if (cell.collapsed == "o") {
      cell.collapsed = "b";
    } else if (cell.collapsed == "b") {
      cell.collapsed = "o";
    } else if (cell.collapsed == "i") {
      cell.collapsed = null;
    } else {
      cell.collapsed = "i";
    }
  }

  function toggle_output_collapsed(e) {
    if (cell.collapsed == "i") {
      cell.collapsed = "b";
    } else if (cell.collapsed == "b") {
      cell.collapsed = "i";
    } else if (cell.collapsed == "o") {
      cell.collapsed = null;
    } else {
      cell.collapsed = "o";
    }
  }

  $: input_collapsed = cell.collapsed == "i" || cell.collapsed == "b";
  $: output_collapsed = cell.collapsed == "o" || cell.collapsed == "b";
</script>

<div
  class="flex flex-col min-w-[250px]"
  on:mouseenter={() => {
    is_hover = true;
  }}
  on:mouseleave={() => {
    is_hover = false;
  }}
>
  <div
    class="flex flex-col items-start w-auto h-auto rounded p-0.25justify-start align-middle"
  >
    <!-- input -->
    {#if !input_collapsed}
      <CodeEditor {cell} bind:focus />
    {:else}
      <div
        class="h-[25px] w-full rounded bg-oli-50 dark:bg-oli-700 border-0 p-0 italic text-[10px] items-center justify-center flex text-oli-500 dark:text-oli-400"
      >
        Code
      </div>
    {/if}

    {#if is_hover}
      <button
        class="absolute h-4 w-4 top-7 -left-[8px] bg-oli-50/50 dark:bg-oli-500/50 rounded border-0 p-0 stroke-oli-500 dark:stroke-oli-200"
        on:click={toggle_input_collapsed}
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          style="
        rotate: {input_collapsed ? '180deg' : '270deg'}"
          ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
            id="SVGRepo_tracerCarrier"
            stroke-linecap="round"
            stroke-linejoin="round"
          ></g><g id="SVGRepo_iconCarrier">
            <path
              d="M15 7L10 12L15 17"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            ></path>
          </g></svg
        >
      </button>
    {/if}

    <!-- output -->
    {#if cell.outputs.length > 0 || cell.state == "running"}
      <!-- <Outputs {cell} /> -->
      <div class="relative w-full">
        {#if !output_collapsed}
          <Outputs {cell} />
        {:else}
          <div
            class=" h-[25px] w-full rounded bg-oli-50 dark:bg-oli-700 border-0 p-0 italic text-[10px] items-center justify-center flex text-oli-500 dark:text-oli-400"
          >
            Output
          </div>
        {/if}

        {#if is_hover}
          <button
            class="absolute h-4 w-4 top-1 -left-[8px] bg-oli-50/50 dark:bg-oli-500/50 rounded border-0 p-0 stroke-oli-500 dark:stroke-oli-200"
            on:click={toggle_output_collapsed}
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              style="
            rotate: {output_collapsed ? '180deg' : '270deg'}"
              ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></g><g id="SVGRepo_iconCarrier">
                <path
                  d="M15 7L10 12L15 17"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                ></path>
              </g></svg
            >
          </button>
        {/if}
      </div>
    {/if}
  </div>
</div>
