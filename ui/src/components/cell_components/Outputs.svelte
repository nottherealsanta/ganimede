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
        border: solid 1px rgba(0, 0, 0, 0.065);
        border-radius: 5px;
        float: bottom;
        margin-top: 1px;
        padding: 4px 3px 4px 3px;
        cursor: default;
        box-shadow: -1px 0px 2px 1px rgba(0, 0, 0, 0.003);
    }

    .output {
        background-color: rgba(255, 255, 255, 0);
        width: fit-content;
        height: fit-content;
        padding: 3px 3px 3px 5px;
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
