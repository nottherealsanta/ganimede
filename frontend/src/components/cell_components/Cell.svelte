<script lang="ts">
  import CodeCell from "./CodeCell.svelte";
  import Grab from "./Grab.svelte";
  import DeleteCell from "./DeleteCell.svelte";

  export let cell_id: string;
  export let index: number;

  import {
    active_cell_id,
    is_command_mode,
    ydoc,
    update_pc_graph,
  } from "../../stores/notebook.js";
  import MarkdownCell from "./MarkdownCell.svelte";
  import NewCellToolbar from "./NewCellToolbar.svelte";
  import LeftControls from "./LeftControls.svelte";

  // cell
  let cell = {
    ycell: ydoc.getMap(cell_id),

    get id() {
      return this.ycell.get("id");
    },
    get type() {
      return this.ycell.get("type");
    },
    get source() {
      return this.ycell.get("source");
    },
    get execution_count() {
      return this.ycell.get("execution_count");
    },
    get execution_time() {
      return this.ycell.get("execution_time");
    },
    get outputs() {
      return this.ycell.get("outputs");
    },
    get heading_level() {
      return this.ycell.get("heading_level");
    },
    get collapsed() {
      return this.ycell.get("collapsed");
    },
    get parent_collapsed() {
      return this.ycell.get("parent_collapsed");
    },
    get state() {
      return this.ycell.get("state");
    },

    set id(value) {
      console.error("ID is read-only");
    },
    set type(value) {
      this.ycell.set("type", value);
    },
    set source(value) {
      this.ycell.set("source", value);
    },
    set execution_count(value) {
      console.error("Execution count is read-only");
    },
    set execution_time(value) {
      console.error("Execution time is read-only");
    },
    set outputs(value) {
      console.error("Outputs is read-only");
    },
    set heading_level(value) {
      this.ycell.set("heading_level", value);
    },
    set collapsed(value) {
      this.ycell.set("collapsed", value);
    },
    set parent_collapsed(value) {
      this.ycell.set("parent_collapsed", value);
    },
    set state(value) {
      console.error("State is read-only");
    },
  };

  // reactivity
  cell.ycell.observe((yevent) => {
    cell = cell; // force reactivity
  });

  // hover
  let is_hover: boolean = false;

  // active cell
  $: is_active = $active_cell_id === cell_id;

  // scroll to active cell
  let cell_div: HTMLDivElement;
  $: if (is_active && cell_div) {
    cell_div.scrollIntoView({
      behavior: "instant",
      block: "nearest",
    });
  }

  // heading level
  $: if (cell.type === "markdown") {
    // @ts-ignore
    cell.ycell
      .get("source")
      .observe((yevent: { target: { toJSON: () => any } }) => {
        const source = yevent.target.toJSON() as string; // If you know it's a string
        const heading_level = source.match(/^#+/)?.[0]?.length || null;
        if (heading_level !== cell.heading_level) {
          cell.heading_level = heading_level;
          update_pc_graph();
        }
      });
  }

  // markdown
  $: is_markdown = cell.type === "markdown";
</script>

<div class={cell.parent_collapsed ? "cell-parent-collapse" : ""}>
  <NewCellToolbar {index} />
</div>
<div
  class="cell
  {is_markdown ? 'border-transparent' : 'border-gray-100'}
  {is_hover ? 'ring-1 ring-gray-200' : ''}
  {is_active ? 'ring-2 ring-gray-100 ' : ''}
  {cell.parent_collapsed ? 'cell-parent-collapse' : ''}
  "
  role="presentation"
  on:mouseenter={() => {
    is_hover = true;
  }}
  on:mouseleave={() => {
    is_hover = false;
  }}
  bind:this={cell_div}
>
  <!-- Cell Controls -->
  <Grab {is_hover} />
  <DeleteCell {cell_id} {is_hover} />
  <LeftControls {cell} {is_hover} />

  <!-- Code / Markdown -->
  {#if !is_markdown}
    <CodeCell {cell} {is_hover} />
  {:else}
    <MarkdownCell {cell} {is_hover} />
  {/if}

  <!-- debug -->
  <!-- <div class="debug">
    <p>{cell_id}</p>
    <p>{cell.type}</p>
    <p>{cell.heading_level}</p>
    <p>{cell.parent_collapsed}</p>
  </div> -->
  <!----------->

  <!-- Active -->
  {#if is_active}
    <div class="active-cell-indicator"></div>
  {/if}
  <!-- Active & Editable -->
  {#if is_active && !$is_command_mode}
    <div class="active-editable-cell-indicator"></div>
  {/if}
</div>

<style>
  .cell {
    @apply flex flex-col relative
    w-auto h-auto mb-1
    bg-white
    rounded-md
    border-2;
    scroll-margin: 20px;
  }
  .cell::before {
    /* for hover effect to work on grab */
    content: "";
    @apply absolute
    top-0 -left-8
    w-8 h-full
    bg-transparent;
  }
  .cell::after {
    /* for hover effect to work on delete */
    content: "";
    @apply absolute
    top-0 -right-8
    w-8 h-full
    bg-transparent;
  }
  .active-cell-indicator {
    width: calc(100% + 35px);
    height: calc(100%);
    top: 0px;
    left: -32px;
    @apply absolute
    w-1 h-full
    rounded-sm
    bg-blue-500;
    pointer-events: none;
  }

  .active-editable-cell-indicator {
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    top: -2px;
    left: -2px;
    @apply absolute
    bg-transparent
    ring-2 ring-blue-500
    rounded-md;
    pointer-events: none;
  }

  .cell-parent-collapse {
    display: none;
  }
  /* 
  .debug {
    @apply absolute bottom-0 right-0
    bg-gray-200/20
    rounded-md
    text-gray-400

    p-1;
    font-family: monospace;
    font-size: 0.6rem;
  } */
</style>
