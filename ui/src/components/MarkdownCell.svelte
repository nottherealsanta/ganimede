<script>
    import { id_map, cells } from "../stores/notebook";

    export let cell_id;
    export let is_tissue = false;

    $: cell = $cells[$id_map[cell_id]];
    // $: is_heading = cell.source[0].startsWith("#");
    $: is_heading = false;

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

<div
    class="{is_tissue
        ? 'w-full'
        : 'w-fit'} flex flex-row items-start h-auto justify-left align-middle p-1"
>
    {#if !is_tissue}
        <div class="w-[25px] h-full pointer-events-none bg-oli-50" />
    {/if}
    <div
        class="{is_tissue ? 'w-full h-full' : 'w-fit h-fit'} 
        bg-oli dark:bg-vs-dark w-fit h-fit min-w-[200px] min-h-[25px] max-w-[616px] text-oli-800 dark:text-oli-200 border-l-2 border-black dark:border-white cursor-text pointer-events-auto"
        on:mousedown={(e) => e.stopPropagation()}
        style={is_tissue ? "background-color:transparent;" : ""}
        use:editor
    />
</div>
