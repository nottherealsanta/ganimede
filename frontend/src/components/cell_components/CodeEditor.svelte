<script context="module">
  let monaco = import("monaco-editor");
</script>

<script lang="ts">
  export let cell;
  export let is_hover: boolean = false;

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
        container.style.height = `${contentHeight + 4}px`;
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
      width = code_editor_container ? code_editor_container.clientWidth - 6 : 0;
      updateHeightWidth();
    }).observe(code_editor_container);
  });

  import { cell_maps } from "../../scripts/test_nb";
  import { onMount } from "svelte";
  import Collapsible from "../utility_components/Collapsible.svelte";

  let code_collapsed: boolean = false;
  let source: string = cell.source;
</script>

<div class="code-editor" bind:this={code_editor_container}>
  <div
    class="editor"
    style="display: {code_collapsed ? 'none' : 'block'}"
    bind:this={container}
  ></div>

  <!-- if collapsed -->
  {#if code_collapsed && cell.source.length > 1}
    <button class="collapsed-editor" on:click={() => (code_collapsed = false)}>
      {cell.source[0]}...
    </button>
  {/if}
  {#if is_hover && cell.source.length > 1}
    <Collapsible bind:is_collapsed={code_collapsed} />
  {/if}
</div>

<style>
  .code-editor {
    @apply flex flex-col relative
    w-full h-fit 
    bg-gray-50
    p-0.5
    min-h-6 
    rounded-b;
  }
  .editor {
    @apply w-full rounded-md bg-gray-50 px-1;
    overflow: visible;
  }
  .collapsed-editor {
    @apply flex
    w-full h-10
    px-4
  bg-gray-50
  text-gray-500
    text-sm
    items-center 
    z-10;
    font-family: "IBM Plex Mono";
  }
  .collapsed-editor:hover {
    @apply bg-gray-100;
  }
</style>
