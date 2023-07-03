<script lang="ts">
    export let output;

    $: if (output["data"]) {
        if (output["data"]["text/plain"]) {
            output["text"] = output["data"]["text/plain"];
        }
    } else {
        output["text"] = output["text"];
    }
</script>

<div
    class="w-fit max-w-3xl h-auto bg-transparent hover:bg-gray-100 dark:hover:bg-zinc-700 pl-1 pr-1 pt-0.5 pb-0.5 rounded whitespace-pre-line overflow-hidden text-xs select-text dark:text-white"
>
    {output["text"].join(" ")}
</div>
