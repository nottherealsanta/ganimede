<script>
    import Cell from "./Cell.svelte";
    import Tissue from "./Tissue.svelte";
    import { id_map, cells } from "../stores/notebook";

    export let cell_id;

    $: cell = $cells[$id_map[cell_id]];
    $: is_heading = cell.source[0].startsWith("#");

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
</script>

{#if is_heading}
    <Tissue {cell_id}>
        <div
            class="w-full h-fit my-0.5 mx-0.25 rounded min-w-[200px] min-h-[25px] max-w-[616px] text-white"
            use:editor
        />
    </Tissue>
{:else}
    <Cell {cell_id}>
        <div class="flex items-start w-fit h-auto justify-center align-stretch">
            <div class="w-6 h-6" />
            <div
                class="bg-gray-50 dark:bg-neutral-800 w-fit h-fit rounded min-w-[200px] min-h-[25px] max-w-[616px]"
                use:editor
            />
        </div>
    </Cell>
{/if}
