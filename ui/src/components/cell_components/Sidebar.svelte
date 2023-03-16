<script>
    export let done;

    export let primary_button_click = () => {};

    export let run_promise;
</script>

<div class="sidebar" id="sidebar">
    <div
        class="primary-button"
        on:click={primary_button_click}
        on:keydown={primary_button_click}
    >
        {#if !done}
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
                <circle cx="27.5" cy="27.5" r="25" />
            </svg>
        {:else}
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
        {/if}
    </div>
</div>

<style>
    .sidebar {
        width: 25px;
        border-radius: 5px;
        float: left;
        flex-direction: column;
        padding-top: 2px;
        padding-right: 2px;
    }
    .primary-button {
        width: 100%;
        height: 25px;
        background-color: rgba(255, 255, 255, 0);
        border-radius: 5px;
        cursor: default;
        display: flex;
        align-items: center;
    }
    .primary-button:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }
    .primary-button:active {
        background-color: rgba(0, 0, 0, 0.2);
    }
    .run-button-svg {
        color: #000000;
        margin: 0 auto;
        display: block;
    }

    @media (prefers-color-scheme: dark) {
        .run-button-svg {
            color: #ffffff;
        }
    }
</style>
