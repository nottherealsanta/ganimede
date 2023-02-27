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

    export let code = "";
    export let language = "python";
    export let focus = false;
    export let height = 0;
    export let width = 0;
    export let max_width = 616;

    import { onMount } from "svelte";
    let monaco;
    let container;
    let editor;
    let n_lines = 1;
    let max_columns = 0;

    $: height = Math.ceil(n_lines * 19);
    $: width = Math.ceil(max_columns * 8) + 50;
    $: width = Math.min(width, max_width);
    $: console.log("max_columns", max_columns, "width", width);

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
    let destroyed;
    onMount(() => {
        monaco = _monaco;
        editor = monaco.editor.create(container, {
            value: code,
            language: language,
            theme: "vs",
            minimap: {
                enabled: false,
            },
            overviewRulerBorder: false,
            overviewRulerLanes: 0,
            renderLineHighlight: "none",
            lineNumbers: config.monaco.lineNumbers,
            fontSize: config.monaco.fontSize,
            glyphMargin: false,
            lineNumbersMinChars: 2,
            lineDecorationsWidth: 0,
            folding: true,
            automaticLayout: true, // updates height when `value` changes
            wordWrap: "on",
            wrappingColumn: 80,
            scrollbar: {
                vertical: "hidden",
                horizontal: "hidden",
                handleMouseWheel: false,
            },
            scrollBeyondLastLine: false,
        });
        editor.onDidFocusEditorText(() => {
            focus = true;
        });
        editor.onDidBlurEditorText(() => {
            focus = false;
        });

        editor.onDidChangeModelContent((e) => {
            max_columns = get_max_columns();
            n_lines = editor._modelData.viewModel.getLineCount();
            code = editor.getValue();
        });
        n_lines = editor.getModel().getLineCount();
        max_columns = get_max_columns();

        return () => {
            destroyed = true;
        };
    });
</script>

<div class="cell-input" style="height: {height}px; width: {width}px;">
    <div class="codeeditor" bind:this={container} />
</div>

<style>
    .cell-input {
        display: flex;
        overflow: hidden;
        height: 100%;
        width: 100%;
        float: top;
        position: relative;
        border-radius: 5px;
        background-color: transparent;
        min-height: 25px;
        min-width: 300px;
    }

    .codeeditor {
        width: 100%;
        height: 100%;
        cursor: default;
        /* align-self: flex-start; */
        /* position: relative; */
    }
</style>
