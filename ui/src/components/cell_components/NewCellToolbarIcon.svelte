<script lang="ts">
    export let icon_name;

    import Connector from "./Icons/connector.svelte";
    import Python from "./Icons/python.svelte";
    import Markdown from "./Icons/markdown.svelte";
    import Disconnect from "./Icons/disconnect.svelte";
    import NewCellMenu from "./Icons/newCellMenu.svelte";

    let icon = null;

    if (icon_name == "connector") {
        icon = Connector;
    } else if (icon_name == "python") {
        icon = Python;
    } else if (icon_name == "markdown") {
        icon = Markdown;
    } else if (icon_name == "disconnect") {
        icon = Disconnect;
    } else if (icon_name == "newCellMenu") {
        icon = NewCellMenu;
    }
</script>

<div class="w-full h-full flex justify-center items-center p-0.5">
    {#if icon}
        <svelte:component this={icon} />
    {/if}
</div>
