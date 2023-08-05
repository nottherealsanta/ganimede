<script>
  import { onMount } from "svelte";

  import { config } from "../stores/config";
  import { MonacoBinding } from "y-monaco";

  import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";

  export let cell;

  let language = "markdown";

  $: source = cell.source.toString();

  cell.source.observe(() => {
    source = cell.source.toString();
  });

  export let focus = false;
  let height = 0;
  let width = 0;
  let max_width = 800;
  let min_min_width = 250;

  let monaco;
  let container;
  let editor;
  let max_columns = 0;
  let div = null;

  let n_lines = 0;
  $: n_lines = cell.source.toString().length;

  $: width = Math.ceil(max_columns * 8) + 40;
  $: width = Math.min(width, max_width);
  $: width = Math.max(width, min_min_width);

  function get_max_columns() {
    let max = 0;
    let _source = cell.source.toString().split("\n");
    for (let i = 0; i < _source.length; i++) {
      let column = _source[i].length;
      if (column > max) {
        max = column;
      }
    }
    return max;
  }

  // dark-light mode
  let theme = {
    dark: "vs-dark",
    light: "light-theme",
  };
  // -- current theme
  let current_theme = window.matchMedia("(prefers-color-scheme: dark)").matches
    ? theme.dark
    : theme.light;
  // -- watch for dark mode changes
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", (event) => {
      // TODO: if theme is not set in config, then auto change;
      if (event.matches) {
        monaco.editor.setTheme(theme.dark);
      } else {
        monaco.editor.setTheme(theme.light);
      }
    });

  // monaco config
  let monaco_config = {
    value: "",
    language: language,
    theme: current_theme,
    minimap: {
      enabled: false,
    },
    overviewRulerBorder: false,
    overviewRulerLanes: 0,
    renderLineHighlight: "none",
    lineNumbers: "off",
    fontSize: config.monaco.fontSize,
    fontFamily: "Fira Code, monospace",
    glyphMargin: false,
    lineNumbersMinChars: 0,
    lineDecorationsWidth: 0,
    folding: false,
    automaticLayout: true, // updates height when `value` changes
    wordWrap: "on",
    wrappingStrategy: "advanced",
    wrappingColumn: 80,
    scrollbar: {
      vertical: "hidden",
      horizontal: "hidden",
      handleMouseWheel: false,
    },
    scrollBeyondLastLine: false,
    overviewRulerLanes: 0,
  };

  let destroyed;

  const mount_monaco = async () => {
    monaco = await import("monaco-editor");

    editor = monaco.editor.create(container, monaco_config);

    // --- import theme
    import("monaco-themes/themes/Active4D.json").then((data) => {
      monaco.editor.defineTheme("light-theme", data);
    });

    // --- set theme
    monaco.editor.setTheme("light-theme");

    max_columns = get_max_columns();

    editor.onDidFocusEditorText(() => {
      focus = true;
    });
    editor.onDidBlurEditorText(() => {
      focus = false;
    });

    editor.onDidChangeModelContent((e) => {
      max_columns = get_max_columns();
    });

    let ignoreEvent = false;
    const updateHeight = () => {
      const contentHeight = Math.min(1000, editor.getContentHeight());
      if (container !== null) {
        container.style.height = `${contentHeight}px`;
        try {
          ignoreEvent = true;
          editor.layout({ width, height: contentHeight });
        } finally {
          ignoreEvent = false;
        }
      }
    };

    editor.onDidContentSizeChange(updateHeight);
    updateHeight();

    // y-monaco
    const monacoBinding = new MonacoBinding(
      cell.source,
      editor.getModel(),
      new Set([editor]),
    ); // TODO: add awareness

    return () => {
      destroyed = true;
    };
  };

  onMount(() => {
    current_theme = window.matchMedia("(prefers-color-scheme: dark)").matches
      ? theme.dark
      : theme.light;
    mount_monaco();
    if (div) {
      div.addEventListener("mousedown", (e) => {
        e.stopPropagation();
      });
      div.addEventListener("mouseup", (e) => {
        e.stopPropagation();
      });
      div.addEventListener("click", () => {
        if (focus === false) {
          editor.focus();
          setTimeout(() => {
            editor.focus();
          }, 100);
          const position = {
            lineNumber: editor.getModel().getLineCount(),
            column:
              editor.getModel().getLineContent(editor.getModel().getLineCount())
                .length + 1,
          };
          editor.setPosition(position, true);
        }
        focus = true;
      });
    }
  });

  import { marked } from "marked";
</script>

<div
  class="h-fit bg-oli dark:bg-oli-800 rounded cell-input py-0.5 pl-1 overflow-hidden relative align-middle cursor-text pointer-events-auto"
  style="min-width: min-content; width: {width}px"
  id="cell-input"
  bind:this={div}
>
  <div
    class="w-full h-fit px-1 rounded text-[14px]"
    style="display: {focus ? 'none' : 'block'}; font-family: IBM Plex Sans"
  >
    {#if editor}
      {@html marked(source)}
    {/if}
  </div>
  <div
    class="w-full cursor-text"
    bind:this={container}
    style="
        width: {width}px; 
        display: {focus ? 'block' : 'none'};
        background-color: {focus ? 'bg-oli' : 'bg-transparent'}"
  />
</div>
