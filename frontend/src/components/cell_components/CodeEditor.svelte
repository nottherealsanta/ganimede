<script context="module">
  let monaco = import("monaco-editor");
</script>

<script lang="ts">
  import { onMount } from "svelte";
  import { MonacoBinding } from "y-monaco";
  import Collapsible from "../utility_components/Collapsible.svelte";

  export let cell;
  // let source = "";

  export let is_hover: boolean = false;

  let code_collapsed: boolean = false;
  let editor: any;

  import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
  self.MonacoEnvironment = {
    getWorker(_, label) {
      return new editorWorker();
    },
  };

  function debounce<T extends Function>(cb: T, wait = 10) {
    let h = 0;
    let callable = (...args: any) => {
      clearTimeout(h);
      h = setTimeout(() => cb(...args), wait);
    };
    return <T>(<any>callable);
  }

  // theme import
  import { light_theme } from "../../scripts/themes";
  let container: HTMLDivElement;
  let code_editor_container: HTMLDivElement;
  let resizeObserver: ResizeObserver;

  let monaco_config: any = {
    value: "",
    language: cell.type === "code" ? "python" : "markdown",
    theme: "vs-light",
    minimap: {
      enabled: false,
    },
    overviewRulerBorder: false,
    overviewRulerLanes: 0,
    renderLineHighlight: "none",
    lineNumbers: cell.type === "code" ? "on" : "off",
    fontSize: 14,
    fontFamily: cell.type === "code" ? "IBM Plex Mono" : "Inter",
    fontLigatures: true,
    fontWeight: "400",
    glyphMargin: false,
    lineNumbersMinChars: cell.type === "code" ? 2 : 0,
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
    editor = monaco.editor.create(container, monaco_config);

    // binding
    const monacoBinding = new MonacoBinding(
      cell.source,
      editor.getModel(),
      new Set([editor])
    ); // TODO: add awareness

    // themes
    // import("../../assets/monaco_themes/light.json").then(data => {
    //   monaco.editor.defineTheme('light', data);
    // })
    monaco.editor.defineTheme("light", light_theme);
    monaco.editor.setTheme("light");

    // dynamic height
    let ignoreEvent = false;
    let width = container.clientWidth;

    const updateHeightWidth = debounce(() => {
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
    });
    editor.onDidContentSizeChange(updateHeightWidth);
    updateHeightWidth();

    // dynamic width
    new ResizeObserver(() => {
      width = code_editor_container ? code_editor_container.clientWidth - 6 : 0;
      updateHeightWidth();
    }).observe(code_editor_container);
  });

  import { active_cell_id, is_command_mode } from "../../stores/notebook.js";
  $: is_active = $active_cell_id === cell.id;
  $: if (is_active && !$is_command_mode) {
    if (editor) {
      setTimeout(() => {
        editor.focus();
      }, 50);
    }
  }
</script>

<div class="code-editor" bind:this={code_editor_container}>
  <div
    class="editor"
    style="display: {code_collapsed ? 'none' : 'block'}"
    bind:this={container}
  ></div>

  <!-- if collapsed -->
  {#if code_collapsed}
    <button class="collapsed-editor" on:click={() => (code_collapsed = false)}>
      <span>Code Hidden</span>&nbsp;
      {cell.source[0]}...
    </button>
  {/if}
  {#if is_hover}
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
    m-0.5
    px-4
  bg-gray-50
  text-gray-600
    text-sm
    items-center 
    z-10;
    font-family: "IBM Plex Mono";
  }
  .collapsed-editor:hover {
    @apply bg-gray-100;
  }
  .collapsed-editor span {
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 600;
  }
</style>
