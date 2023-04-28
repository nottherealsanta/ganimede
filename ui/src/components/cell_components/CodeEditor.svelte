<script context="module">
    let monaco_promise;
    let _monaco;
    monaco_promise = import("./monaco.js");
    monaco_promise.then((mod) => {
        _monaco = mod.default;
    });
</script>

<script lang="ts">
    import { config } from "../../stores/config";
    import { notebook, id_map } from "../../stores/notebook";

    export let cell_id;

    $: cell = $notebook["cells"][$id_map[cell_id]];

    let language = "";
    $: if (cell) {
        if (cell.cell_type === "markdown") {
            language = "markdown";
        } else {
            language = "python";
        }
    }
    export let focus = false;
    let height = 0;
    let width = 0;
    let max_width = 616;

    import { onMount } from "svelte";
    let monaco;
    let container;
    let editor;
    let n_lines = 1;
    let max_columns = 0;

    $: height = Math.ceil(n_lines * 21);
    $: width = Math.ceil(max_columns * 8) + 50;
    $: width = Math.min(width, max_width);
    let value = "";
    $: if ($notebook["cells"][$id_map[cell_id]].source !== "") {
        value = $notebook["cells"][$id_map[cell_id]].source.join("");
    }

    function get_max_columns() {
        let max = 0;
        for (let i = 0; i < editor.getModel().getLineCount(); i++) {
            let column = editor.getModel().getLineMaxColumn(i + 1);
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
    $: monaco_config = {
        value: value,
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
        wrappingColumn: 80,
        scrollbar: {
            vertical: "hidden",
            horizontal: "hidden",
            handleMouseWheel: false,
        },
        scrollBeyondLastLine: false,
    };

    let destroyed;
    onMount(() => {
        monaco = _monaco;
        editor = monaco.editor.create(container, monaco_config);

        editor.onDidFocusEditorText(() => {
            focus = true;
        });
        editor.onDidBlurEditorText(() => {
            focus = false;
        });

        editor.onDidChangeModelContent((e) => {
            max_columns = get_max_columns();
            n_lines = editor._modelData.viewModel.getLineCount();
            $notebook["cells"][$id_map[cell_id]].source = editor
                .getValue()
                .split("\n");
        });

        n_lines = editor.getModel().getLineCount();
        max_columns = get_max_columns();

        return () => {
            destroyed = true;
        };
    });
</script>

<!-- <style>
    .cell-input {
        display: flex;
        overflow: hidden;
        float: top;
        position: relative;
        border: solid 1px rgba(0, 0, 0, 0.15);
        border-radius: 4px;
        background-color: transparent;
        min-height: 25px;
        min-width: 150px;
        /* box-shadow: -1px 0px 2px 1px rgba(0, 0, 0, 0.048); */
    }

    .codeeditor {
        width: 100%;
        height: 100%;
        cursor: text;
        margin: 3px 0px 3px 0px;
    }
</style> -->

<div
    class="flex overflow-hidden relative border rounded border-zinc-100 dark:border-neutral-800 bg-transparent align-middle"
    style="height: {height}px; width: {width}px; min-height: 25px; min-width: 150px;"
    id="cell-input"
>
    <div
        class="w-full h-full cursor-text"
        style=" margin: 3px 0px 3px 0px;"
        bind:this={container}
    />
</div>
