<script>
    import { send_message } from "../../stores/socket";

    async function interrupt_kernel() {
        send_message({
            channel: "kernel",
            method: "interrupt",
            message: {},
        });
    }
</script>

<div
    class="opacity-70 hover:opacity-100 fixed flex flex-row self-center top-2 align-center items-center w-[500px] h-8 pl-6 bg-oli dark:bg-neutral-800 border rounded-full border-neutral-300 dark:border-neutral-700 justify-left align-middle pointer-events-auto"
    style="
    left: 50%;
    transform: translate(-50%, 50%);
    "
>
    <button
        class="h-fit w-fit m-0 p-0 flex align-middle justify-center items-center self-center hover:bg-oli-600/50 active:bg-neutral-200/20 rounded-sm border border-oli-100 dark:border-oli-800 text-oli-400 dark:hover:bg-oli-600 dark:hover:text-white dark:active:bg-oli-600 dark:active:text-oli"
        on:click={interrupt_kernel}
        alt="Interrupt Kernel"
    >
        <svg width="9" height="9">
            <rect width="10" height="10" class="fill-current" />
        </svg>
    </button>
</div>
