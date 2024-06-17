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
  import { activeCellId } from "../../stores/notebook";
  $: is_active = $activeCellId === cell_id;

  // -- when active focus the textarea
  let textarea: HTMLTextAreaElement;
  $: if (is_active) {
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
</script>

<div class="markdown">
  <textarea
    class="textarea {is_active ? 'block' : 'hidden'}"
    bind:value={source}
    bind:this={textarea}
    on:input={() => {
      cell.source = source.split("\n");
      adjustHeight(); // Add this line
    }}
  ></textarea>
  <div class="{is_active ? 'hidden' : ''} markdown-content">
    {@html marked(source)}
  </div>
</div>

<style>
  .markdown {
    @apply flex flex-col
    w-full min-h-10
    px-4 py-0
    bg-transparent
    items-start justify-center
    text-gray-900
    rounded-md
    overflow-y-auto
    border border-transparent;
    font-family: "Inter", sans-serif;
  }
  .markdown:hover {
    @apply border border-gray-200;
  }
  .textarea {
    @apply w-full h-full
    py-2
    bg-transparent
    border-none
    resize-none
    outline-none;
    font-family: "Inter", sans-serif;
    min-height: 50px;
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
