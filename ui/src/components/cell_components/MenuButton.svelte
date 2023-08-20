<script>
  export let cell;
  async function click() {
    console.log(cell);
  }
</script>

<div
  class="flex flex-none bg-transparent hover:bg-oli-100 dark:hover:bg-oli-800 active:bg-oli-200 dark:active:bg-oli-700 w-5 h-5 p-0.5 m-0 rounded-sm items-center justify-center stroke-oli-600 dark:stroke-white fill-oli-600 dark:fill-white cursor-pointer pointer-events-auto"
  on:mousedown|stopPropagation={(e) => {
    click();
  }}
>
  <svg
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 20 20"
    width="12px"
    height="12px"
  >
    <path
      fill-rule="evenodd"
      d="M 3 9 A 1 1 0 0 0 3 12 A 1 1 0 0 0 3 9 M 10 9 A 1 1 0 0 0 10 12 A 1 1 0 0 0 10 9 m 7 0 A 1 1 0 0 0 17 12 A 1 1 0 0 0 17 9"
      clip-rule="evenodd"
    /></svg
  >
</div>
