<script context="module">
  let monaco = import("monaco-editor");
</script>

<script lang="ts">
  import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
  self.MonacoEnvironment = {
    getWorker(_, label) {
      return new editorWorker();
    },
  };

  let container: HTMLDivElement;
  let code_editor_container: HTMLDivElement;

  let monaco_config: any = {
    value: "",
    language: "python",
    theme: "vs-light",
    minimap: {
      enabled: false,
    },
    overviewRulerBorder: false,
    overviewRulerLanes: 0,
    renderLineHighlight: "none",
    lineNumbers: "on",
    fontSize: 13,
    fontFamily: "Fira Code, monospace",
    glyphMargin: false,
    lineNumbersMinChars: 2,
    lineDecorationsWidth: 0,
    folding: true,
    automaticLayout: true, // updates height when `value` changes
    wordWrap: "on",
    wrappingStrategy: "advanced",
    wrappingColumn: 80,
    scrollbar: {
      vertical: "hidden",
      horizontal: "hidden",
      // handleMouseWheel: false,
    },
    scrollBeyondLastLine: false,
  };
  onMount(async () => {
    const monaco = await import("monaco-editor");
    const editor = monaco.editor.create(container, monaco_config);

    // dynamic height
    let ignoreEvent = false;
    let width = container.clientWidth;

    const updateHeight = () => {
      const contentHeight = Math.max(
        24,
        Math.min(1000, editor.getContentHeight())
      );
      container.style.width = `${width}px`;
      container.style.height = `${contentHeight}px`;
      try {
        ignoreEvent = true;
        editor.layout({ width, height: contentHeight });
      } finally {
        ignoreEvent = false;
      }
    };
    editor.onDidContentSizeChange(updateHeight);
    updateHeight();

    // dynamic width
    // new ResizeObserver(() => console.log("resizing")).observe(
    //   code_editor_container
    // );
    new ResizeObserver(() => {
      console.log("resizing");
      width = code_editor_container.clientWidth - 32;
      updateHeight();
    }).observe(code_editor_container);
  });

  import { cell_maps } from "../../scripts/test_nb";
  import { onMount } from "svelte";

  export let cell_id: string;

  let cell: any = cell_maps[cell_id];
  let source: string = cell.source;
</script>

<div class="code-editor" bind:this={code_editor_container}>
  <div class="editor" bind:this={container}></div>
</div>

<style>
  .code-editor {
    @apply flex flex-col
    w-full h-fit 
    min-h-8 
    pt-2 pb-1
    bg-white
    rounded;
  }
  .editor {
    @apply w-full;
  }
</style>
