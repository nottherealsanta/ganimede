<script context="module">
  let monaco = import("monaco-editor");
</script>

<script lang="ts">
  export let cell;

  import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
  self.MonacoEnvironment = {
    getWorker(_, label) {
      return new editorWorker();
    },
  };

  // theme import
  import { light_theme } from "../../scripts/themes";
  let container: HTMLDivElement;
  let code_editor_container: HTMLDivElement;

  let monaco_config: any = {
    value: cell.source.join(""),
    language: cell.type,
    theme: "vs-light",
    minimap: {
      enabled: false,
    },
    overviewRulerBorder: false,
    overviewRulerLanes: 0,
    renderLineHighlight: "none",
    lineNumbers: "on",
    fontSize: 14,
    fontFamily: "IBM Plex Mono",
    fontLigatures: true,
    fontWeight: "400",
    glyphMargin: false,
    lineNumbersMinChars: 2,
    lineDecorationsWidth: 0,
    folding: true,
    automaticLayout: true, // updates height when `value` changes
    wordWrap: "on",
    wrappingStrategy: "advanced",
    wrappingColumn: 80,
    bracketPairColorization: true,
    scrollbar: {
      vertical: "hidden",
      horizontal: "hidden",
      handleMouseWheel: false,
    },
    scrollBeyondLastLine: false,
  };
  onMount(async () => {
    const monaco = await import("monaco-editor");
    const editor = monaco.editor.create(container, monaco_config);

    // themes
    // import("../../assets/monaco_themes/light.json").then(data => {
    //   monaco.editor.defineTheme('light', data);
    // })
    monaco.editor.defineTheme("light", light_theme);
    monaco.editor.setTheme("light");

    // dynamic height
    let ignoreEvent = false;
    let width = container.clientWidth;

    const updateHeightWidth = () => {
      const contentHeight = Math.max(
        25,
        Math.min(2000, editor.getContentHeight())
      );
      if (container) {
        container.style.width = `${width}px`;
        container.style.height = `${contentHeight + 8}px`;
      }
      try {
        ignoreEvent = true;
        editor.layout({ width, height: contentHeight });
      } finally {
        ignoreEvent = false;
      }
    };
    editor.onDidContentSizeChange(updateHeightWidth);
    updateHeightWidth();

    // dynamic width
    new ResizeObserver(() => {
      width = code_editor_container ? code_editor_container.clientWidth - 4 : 0;
      updateHeightWidth();
    }).observe(code_editor_container);
  });

  import { cell_maps } from "../../scripts/test_nb";
  import { onMount } from "svelte";

  let source: string = cell.source;
</script>

<div class="code-editor" bind:this={code_editor_container}>
  <div class="editor" bind:this={container}></div>
</div>

<style>
  .code-editor {
    @apply flex flex-col
    w-full h-fit 
    p-0.5
    min-h-6 
    bg-gray-50/50
    rounded-b;
  }
  .editor {
    @apply w-full rounded-md bg-gray-50/50 py-1;
    overflow: hidden;
  }
</style>
