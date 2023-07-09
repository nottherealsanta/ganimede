<script>
    import { id_map, cells, pc_graph } from "../stores/notebook";

    export let cell_id;
    export let is_tissue = false;

    $: cell = $cells[$id_map[cell_id]];
    // $: is_heading = cell.source[0].startsWith("#");
    // $: is_heading = false;

    import { Editor, rootCtx, defaultValueCtx } from "@milkdown/core";
    import { commonmark } from "@milkdown/preset-commonmark";
    import { listener, listenerCtx } from "@milkdown/plugin-listener";

    function editor(dom) {
        Editor.make()
            .config((ctx) => {
                ctx.set(rootCtx, dom);
                ctx.set(defaultValueCtx, cell.source.join(""));
                const listener = ctx.get(listenerCtx);

                listener.markdownUpdated((ctx, markdown, prevMarkdown) => {
                    if (markdown !== prevMarkdown) {
                        $cells[$id_map[cell_id]].source =
                            markdown.split("\n\n");
                    }
                });
            })
            .use(listener)
            .use(commonmark)
            .create();
    }

    import DeleteButton from "./cell_components/DeleteButton.svelte";
    import Drag from "../components/cell_components/Icons/drag.svelte";
    import MenuButton from "./cell_components/MenuButton.svelte";
    let is_hover = false;
</script>

<div
    class="w-fitflex flex-col items-start h-auto align-left"
    on:mouseenter={() => {
        is_hover = true;
    }}
    on:mouseleave={() => {
        is_hover = false;
    }}
>
    <div
        class="'w-fit bg-oli dark:bg-vs-dark w-fit h-fit min-w-[200px] min-h-[25px] max-w-[616px] text-oli-800 dark:text-oli-200 cursor-text pointer-events-auto"
        on:mousedown={(e) => e.stopPropagation()}
        style={is_tissue ? "background-color:transparent;" : ""}
        use:editor
    />
</div>
