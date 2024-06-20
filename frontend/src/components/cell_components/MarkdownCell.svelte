<script lang="ts">
  export let cell_id: string;
  import { cell_maps } from "../../scripts/test_nb";
  let cell: any = cell_maps[cell_id];
  let source = cell.source.join("\n");

  // marked for markdown
  import { marked } from "marked";
  marked.setOptions({
    gfm: true,
  });

  // active cell
  import { active_cell_id, is_command_mode } from "../../stores/notebook";
  import { ChevronDown } from "lucide-svelte";
  $: is_active = $active_cell_id === cell_id;

  // -- when active focus the textarea
  let textarea: HTMLTextAreaElement;
  $: if (is_active && !$is_command_mode) {
    setTimeout(() => {
      if (textarea) {
        textarea.focus();
        textarea.style.height = `${textarea.scrollHeight}px`; // Add this line
      }
    }, 0);
  }

  function adjustHeight() {
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }

  $: show_textarea = is_active && !$is_command_mode;
</script>

<div class="markdown">
  <div
    class="flex absolute top-0 w-8 h-10 justify-center items-center bg-transparent rounded-l-md"
  >
    <ChevronDown class="w-6 h-6 text-gray-500" />
  </div>
  <div class="flex w-full h-full ml-8">
    <textarea
      class="textarea {show_textarea ? 'block' : 'hidden'}"
      bind:value={source}
      bind:this={textarea}
      on:input={() => {
        cell.source = source.split("\n");
        adjustHeight(); // Add this line
      }}
    ></textarea>
    <div class="{show_textarea ? 'hidden' : ''} marked w-full h-fit">
      {@html marked(source)}
    </div>
  </div>
</div>

<style>
  .markdown {
    @apply flex flex-row
    w-full min-h-10
    h-full 
    z-10
    bg-white
    items-center
    text-gray-900
    rounded-md
    overflow-y-auto
    border border-transparent;
  }
  .markdown:hover {
    @apply border border-gray-200;
  }
  .textarea {
    @apply w-full h-full
    px-2 py-2
    bg-gray-50
    border-none
    resize-none
    outline-none
    z-20;
    font-family: "Inter", sans-serif;
  }
  .textarea::selection {
    @apply bg-sky-200;
  }
  .marked {
    @apply w-full h-fit
    px-2
    border-none
    resize-none
    outline-none
    z-20;
    font-family: "Inter", sans-serif;
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
</style>
