<script lang="ts">
  export let cell: any;
  export let is_hover: boolean = false;
  let source = cell.ycell.get("source").toString();

  cell.source.observe((event: any) => {
    source = cell.ycell.get("source").toString();
  });

  // marked for markdown
  import { marked } from "marked";
  marked.setOptions({
    gfm: true,
  });

  // active cell
  import { active_cell_id, is_command_mode } from "../../stores/notebook";
  import CodeEditor from "./CodeEditor.svelte";
  import CellBar from "./CellBar.svelte";
  $: is_active = $active_cell_id === cell.id;

  // -- when active focus the textarea
  let textarea: HTMLTextAreaElement;
  let is_focused = false;
  $: if (is_active && !$is_command_mode) {
    if (textarea && !is_focused) {
      is_focused = true;
      setTimeout(() => {
        console.log("focus");
        textarea.focus();
        textarea.style.height = `0`;
        textarea.style.height = `${textarea.scrollHeight}px`;
      }, 50);
    }
  }

  $: show_textarea = is_active && !$is_command_mode;
</script>

<div
  class="markdown {show_textarea ? 'bg-gray-50' : 'bg-transparent'}"
  on:click={(e) => {
    active_cell_id.set(cell.id);
    $is_command_mode = false;
  }}
  role="presentation"
>
  <div class="flex flex-col w-3/4 h-full p-0">
    <div
      class="{show_textarea
        ? 'h-auto opacity-100 pt-2'
        : 'h-0 opacity-0'} w-full"
    >
      <CodeEditor {cell} />
    </div>
    <div class="{show_textarea ? 'hidden' : ''} marked w-full h-fit">
      {@html marked(source)}
    </div>
  </div>
  <div class="flex w-1/4 h-fit self-start">
    <CellBar {cell} {is_hover} />
  </div>
</div>

<style>
  .markdown {
    @apply flex flex-row
    w-full min-h-8
    h-full 
    p-0
    items-center
    text-gray-900
    rounded-md;
  }

  .marked {
    @apply w-full h-fit
    px-2
    bg-transparent
    border-none
    resize-none
    outline-none;
    font-family: "IBM Plex Sans", sans-serif;
  }
  :global(.markdown p) {
    font-size: 16px;
    font-weight: 400;
    line-height: 1.5;
  }
  :global(.markdown ul) {
    list-style-type: circle;
  }
  :global(.markdown li) {
    margin-left: 2rem;
  }
  :global(.markdown h1) {
    font-weight: 600;
    font-size: 30px;
    line-height: 1.5;
  }
  :global(.markdown h2) {
    font-weight: 500;
    font-size: 20px;
    line-height: 1.5;
  }
  :global(.markdown h3) {
    font-weight: 500;
    font-size: 18px;
    line-height: 1.5;
  }
  :global(.markdown h4) {
    font-weight: 600;
    font-size: 16px;
    line-height: 1.5;
  }
  :global(.markdown h5) {
    font-weight: 600;
    font-size: 14px;
    line-height: 1.5;
  }
  :global(.markdown h6) {
    font-weight: 600;
    font-size: 12px;
    line-height: 1.5;
  }
  :global(.markdown code) {
    padding: 5px;
    border-radius: 5px;
    font-family: "Fira Code", monospace;
  }
  :global(.markdown pre) {
    padding: 10px;
    border-radius: 5px;
  }
  :global(.markdown blockquote) {
    padding: 10px;
    border-left: 3px solid #ccc;
    margin: 1em 0;
  }
  :global(.markdown a) {
    color: #0095ff;
  }
  :global(.markdown a:hover) {
    color: #f60;
  }
  :global(.markdown img) {
    max-width: 100%;
  }
  :global(.markdown em) {
    font-style: italic;
  }
</style>
