<script context="module">
    // let monaco_promise;
    // let _monaco;
    // monaco_promise = import("./monaco.js");
    // monaco_promise.then((mod) => {
    //     _monaco = mod.default;
    //     console.log("monaco loaded");
    // });
</script>

<script>
    import { onMount } from "svelte";

    import { config } from "../../stores/config";
    import { cells, id_map } from "../../stores/notebook";

    import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";

    export let cell_id;

    $: cell = $cells[$id_map[cell_id]];

    let language = "python";

    export let focus = false;
    let height = 0;
    let width = 0;
    let max_width = 1200;
    let min_min_width = 200;

    let monaco;
    let container;
    let editor;
    let max_columns = 0;
    let div = null;

    let n_lines = 0;
    $: n_lines = cell.source.length;

    $: width = Math.ceil(max_columns * 8) + 50;
    $: width = Math.min(width, max_width);
    $: width = Math.max(width, min_min_width);

    $: if (editor) {
        if (editor.getValue() !== $cells[$id_map[cell_id]].source.join("")) {
            $cells[$id_map[cell_id]].source = editor
                .getValue()
                .split("\n")
                .map((line) => (line ? line + "\n" : line));
        }
    }

    function get_max_columns() {
        let max = 0;
        let source = cell.source;
        for (let i = 0; i < source.length; i++) {
            let column = source[i].length;
            if (column > max) {
                max = column;
            }
        }
        return max;
    }

    // dark-light mode
    let theme = {
        dark: "vs-dark",
        light: "vs",
    };
    // -- current theme
    let current_theme = window.matchMedia("(prefers-color-scheme: dark)")
        .matches
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
        value: $cells[$id_map[cell_id]].source.join(""),
        language: language,
        theme: current_theme,
        minimap: {
            enabled: false,
        },
        overviewRulerBorder: false,
        overviewRulerLanes: 0,
        renderLineHighlight: "none",
        lineNumbers: config.monaco.lineNumbers,
        fontSize: config.monaco.fontSize,
        fontFamily: "Fira Code, monospace",
        glyphMargin: false,
        lineNumbersMinChars: 1,
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
    onMount(async () => {
        self.MonacoEnvironment = {
            getWorker: function (_moduleId, label) {
                return new editorWorker();
            },
        };

        monaco = await import("monaco-editor");

        // monaco = _monaco;
        editor = monaco.editor.create(container, monaco_config);

        // editor.setValue(value);

        max_columns = get_max_columns();

        editor.onDidFocusEditorText(() => {
            focus = true;
        });
        editor.onDidBlurEditorText(() => {
            focus = false;
        });

        editor.onDidChangeModelContent((e) => {
            max_columns = get_max_columns();

            // $cells[$id_map[cell_id]].source = editor
            //     .getValue()
            //     .split("\n")
            //     .map((line) => (line ? line + "\n" : line));
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

        return () => {
            destroyed = true;
        };
    });

    onMount(() => {
        // for dragSelect
        if (div) {
            div.addEventListener("mousedown", (e) => {
                e.stopPropagation();
            });
            div.addEventListener("mouseup", (e) => {
                e.stopPropagation();
            });
            div.addEventListener("click", () => {
                editor.focus();
            });
        }
    });
</script>

<div
    class="h-fit bg-white rounded-t cell-input py-0.5 overflow-hidden relative align-middle cursor-text pointer-events-auto"
    style=" min-height: 25px; width:100%;        "
    id="cell-input"
    bind:this={div}
>
    <div
        class="w-full h-full cursor-text"
        bind:this={container}
        style="width: {width}px"
    />
</div>
