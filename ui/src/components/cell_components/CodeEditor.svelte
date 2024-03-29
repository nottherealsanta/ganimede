<script>
  import { onMount, afterUpdate } from "svelte";
  import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
  self.MonacoEnvironment = {
    getWorker(_, label) {
      return new editorWorker();
    },
  };

  import { config } from "../../stores/config";
  import { MonacoBinding } from "y-monaco";
  import { send_message } from "../../stores/socket";

  export let cell;
  let source = cell.source;
  let language = "python";

  export let focus = false;
  let height = 0;
  let width = 0;
  let max_width = 800;
  let min_min_width = 250;

  let monaco;
  let container;
  let editor;
  let max_columns = 0;
  let input_div = null;

  let n_lines = 0;
  $: n_lines = source.toString().length;

  $: width = Math.ceil(max_columns * 9) + 40; // TODO: must be calculated from font size
  $: width = Math.min(width, max_width);
  $: width = Math.max(width, min_min_width);

  function get_max_columns() {
    let max = 0;
    let _source = source.toString().split("\n");
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
    lineNumbers: "on",
    fontSize: config.monaco.fontSize,
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
      handleMouseWheel: false,
    },
    scrollBeyondLastLine: false,
    overviewRulerLanes: 0,
  };

  let destroyed;
  // import * as monaco from "monaco-editor";

  const mount_monaco = async () => {
    monaco = await import("monaco-editor");

    // --- import theme
    await import("monaco-themes/themes/Active4D.json").then((data) => {
      monaco.editor.defineTheme("light-theme", data);
    });

    if (current_theme === theme.light) {
      monaco.editor.setTheme("light-theme");
    } else {
      monaco.editor.setTheme("vs-dark");
    }
    editor = monaco.editor.create(container, monaco_config);

    // --- set theme

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

    // custom keybindings

    // -- run
    editor.addAction({
      id: "run",
      label: "Run",
      keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
      run: () => {
        if (cell.state === "idle") {
          send_message({
            channel: "notebook",
            method: "queue_cell",
            message: {
              cell_id: cell.id,
            },
          });
        }
      },
    });

    // y-monaco
    const monacoBinding = new MonacoBinding(
      source,
      editor.getModel(),
      new Set([editor]),
    ); // TODO: add awareness

    return () => {
      destroyed = true;
    };
  };

  function lines_content_overflow_fix() {
    if (input_div === null) return;
    // get elements that have "lines-content monaco-editor-background" as class
    let lines_content = input_div.getElementsByClassName("lines-content");
    // change their style: width to 100%, height to 100%
    for (let i = 0; i < lines_content.length; i++) {
      lines_content[i].style.width = "100%";
      lines_content[i].style.height = "100%";
    }
  }

  onMount(() => {
    current_theme = window.matchMedia("(prefers-color-scheme: dark)").matches
      ? theme.dark
      : theme.light;
    mount_monaco();
    // for dragSelect
    if (input_div) {
      input_div.addEventListener("mousedown", (e) => {
        e.stopPropagation();
      });
      input_div.addEventListener("mouseup", (e) => {
        e.stopPropagation();
      });
      input_div.addEventListener("click", () => {
        editor.focus();
      });
    }
    // overflow fix
    setTimeout(lines_content_overflow_fix, 500);
  });
</script>

<div
  class="h-fit bg-oli dark:bg-[#1E1E1E] cell-input py-0.5 pl-0 overflow-hidden relative align-middle cursor-text pointer-events-auto
  {cell.outputs.toJSON().length > 0 ? '' : 'rounded-b'}"
  style=" min-height: 25px; width:100%;"
  id="cell-input"
  bind:this={input_div}
>
  <div
    class="h-full cursor-text"
    bind:this={container}
    style="width: {width}px"
  />
</div>
