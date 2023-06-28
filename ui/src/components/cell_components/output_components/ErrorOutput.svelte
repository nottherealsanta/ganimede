<script lang="ts">
    export let output;

    import { default as AnsiUp } from "ansi_up";
    const ansi_up = new AnsiUp();
</script>

<div class="select-text hover:bg-white/50 dark:hover:bg-black/10">
    {#if output["traceback"]}
        {#each output["traceback"] as line}
            <div class="text-gray-800 dark:text-white whitespace-pre font-mono">
                {@html ansi_up.ansi_to_html(line)}
            </div>
        {/each}
    {/if}
</div>
