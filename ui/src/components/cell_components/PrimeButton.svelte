<script>
    export let cell_state;
</script>

<!-- <div>
    {cell_state}
</div> -->
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    viewBox="0 0 55 55"
    fill="none"
    stroke="currentColor"
    stroke-width="3"
    stroke-linecap="round"
    stroke-linejoin="round"
    class="run-button-svg"
>
    <polygon points="19 12 19 43 43 27.5 19 12" />
</svg>

<style>
    .run-button-svg {
        color: #000000;
        margin: 0 auto;
        display: block;
    }
    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .run-button-svg {
            color: rgba(209, 209, 209, 1);
        }
    }
</style>
