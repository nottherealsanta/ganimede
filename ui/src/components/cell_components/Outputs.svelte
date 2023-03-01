<script lang="ts">
</script>

<div class="outputs">
    <div class="output">Hello There!</div>
</div>

<style>
    .outputs {
        width: auto;
        height: fit-content;
        /* background-color: #cccccc; */
        border: solid 1px rgba(215, 215, 215, 0.129);
        border-radius: 5px;
        float: bottom;
        margin-top: 5px;
        padding: 5px 5px 5px 5px;
        cursor: default;
    }

    .output {
        background-color: rgba(255, 255, 255, 0);
        width: fit-content;
        height: fit-content;
        padding: 5px 5px 5px 5px;
        border-radius: 5px;
    }
    .output:hover {
        background-color: rgba(0, 0, 0, 0.031);
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .outputs {
            /* background-color: rgba(211, 211, 211, 0.02); */
            color: #cccccc;
        }
    }
</style>
