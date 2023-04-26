<script lang="ts">
    export let icon_name;

    import Connector from "./Icons/connector.svelte";
    import Python from "./Icons/python.svelte";
    import Markdown from "./Icons/markdown.svelte";

    let icon = null;

    if (icon_name == "connector") {
        icon = Connector;
    } else if (icon_name == "python") {
        icon = Python;
    } else if (icon_name == "markdown") {
        icon = Markdown;
    }
</script>

<div
    class="w-full h-full flex justify-center items-center p-0.5 fill-gray-600 dark:fill-gray-300"
>
    {#if icon}
        <svelte:component this={icon} />
    {/if}
</div>
