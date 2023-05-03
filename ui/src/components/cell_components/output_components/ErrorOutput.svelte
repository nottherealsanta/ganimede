<script lang="ts">
    export let output;

    import { default as AnsiUp } from "ansi_up";
    const ansi_up = new AnsiUp();
</script>

{#if output["traceback"]}
    {#each output["traceback"] as line}
        <div class="text-gray-800 dark:text-gray-200 whitespace-pre font-mono">
            {@html ansi_up.ansi_to_html(line)}
        </div>
    {/each}
{/if}
