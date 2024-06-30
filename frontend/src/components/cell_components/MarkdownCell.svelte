<script lang="ts">
  export let cell: any;
  let source = cell.ycell.get("source").toString();

  // marked for markdown
  import { marked } from "marked";
  marked.setOptions({
    gfm: true,
  });

  // active cell
  import { active_cell_id, is_command_mode } from "../../stores/notebook";
  import CodeEditor from "./CodeEditor.svelte";
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

  function adjustHeight() {
    if (textarea) {
      textarea.style.height = `0`; // this adjusts the height when it decreases
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }

  $: show_textarea = is_active && !$is_command_mode;
</script>

<div
  class="markdown"
  on:click={(e) => {
    active_cell_id.set(cell.id);
    $is_command_mode = false;
  }}
  role="presentation"
>
  <div class="flex flex-col w-full h-full p-0">
    <!-- <textarea
      class="textarea {show_textarea ? 'block' : 'hidden'}"
      bind:value={source}
      bind:this={textarea}
      on:input={() => {
        // cell.source = source.split("\n"); TODO
        adjustHeight(); // Add this line
      }}
    ></textarea> -->
    <div
      class="{show_textarea
        ? 'h-auto opacity-100'
        : 'h-0 opacity-0'} w-full h-fit"
    >
      <CodeEditor {cell} />
    </div>
    <div class="{show_textarea ? 'hidden' : ''} marked w-full h-fit">
      {@html marked(cell.ycell.get("source").toString())}
    </div>
  </div>
</div>

<style>
  .markdown {
    @apply flex flex-row
    w-full min-h-8
    h-full 
    p-0
    z-10
    bg-transparent
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
    outline-none
    z-20;
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
