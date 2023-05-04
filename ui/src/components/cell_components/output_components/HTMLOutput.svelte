<script lang="ts">
    export let output;
</script>

<div
    class="flex w-fit h-fit my-1 hover:bg-gray-100 dark:hover:bg-neutral-700 rounded"
>
    {@html output["data"]["text/html"].join(" ")}
</div>
