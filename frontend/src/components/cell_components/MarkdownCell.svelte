<script lang="ts">
  export let cell_id: string;
  import { cell_maps } from "../../scripts/test_nb";
  let cell: any = cell_maps[cell_id];

  import { marked } from "marked";
  marked.setOptions({
    gfm: true,
  });

  let source = cell.source.join("\n");
</script>

<div class="markdown">
  <p>{@html marked(source)}</p>
</div>

<style>
  .markdown {
    @apply flex flex-col
    w-full h-full
    px-4
    bg-transparent
    text-gray-900
    border-l-2 border-gray-200
    rounded-md
    overflow-y-auto;
    font-family: "Inter", sans-serif;
  }
  :global(.markdown p) {
    font-size: 16px;
    font-weight: 400;
    line-height: 1.6;
    margin-top: 6px;
    margin-bottom: 6px;
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
    line-height: 2;
    margin-top: 4px;
    margin-bottom: 4px;
  }
  :global(.markdown h2) {
    font-weight: 500;
    font-size: 20px;
    line-height: 2;
    margin-top: 4px;
    margin-bottom: 4px;
  }
  :global(.markdown h3) {
    font-weight: 500;
    font-size: 18px;
    line-height: 2;
    margin-top: 4px;
    margin-bottom: 4px;
  }
  :global(.markdown h4) {
    font-weight: 600;
    font-size: 16px;
    line-height: 2;
  }
  :global(.markdown h5) {
    font-weight: 600;
    font-size: 14px;
    line-height: 2;
  }
  :global(.markdown h6) {
    font-weight: 600;
    font-size: 12px;
    line-height: 2;
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
