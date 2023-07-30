<script>
  export let cell;

  async function click() {
    console.log("cell", cell);
  }
</script>

<div
  class="flex flex-none bg-transparent hover:bg-oli-100 dark:hover:bg-oli-800 active:bg-oli-200 dark:active:bg-oli-700 w-5 h-5 pt-0 pr-0 pl-0 pb-0.5 m-0 rounded-sm items-center justify-center stroke-black dark:stroke-white fill-black dark:fill-white cursor-pointer pointer-events-auto"
  on:mousedown|stopPropagation={(e) => {
    click();
  }}
>
  <svg
    width="18px"
    height="18px"
    viewBox="0 0 1024 1024"
    class="icon"
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    ><path
      d="M667.8 362.1H304V830c0 28.2 23 51 51.3 51h312.4c28.4 0 51.4-22.8 51.4-51V362.2h-51.3z"
      fill="#ccc"
      stroke="#000"
      stroke-width="5"
    /><path
      d="M733.3 258.3H626.6V196c0-11.5-9.3-20.8-20.8-20.8H419.1c-11.5 0-20.8 9.3-20.8 20.8v62.3H289.9c-20.8 0-37.7 16.5-37.7 36.8V346c0 18.1 13.5 33.1 31.1 36.2V830c0 39.6 32.3 71.8 72.1 71.8h312.4c39.8 0 72.1-32.2 72.1-71.8V382.2c17.7-3.1 31.1-18.1 31.1-36.2v-50.9c0.1-20.2-16.9-36.8-37.7-36.8z m-293.5-41.5h145.3v41.5H439.8v-41.5z m-146.2 83.1H729.5v41.5H293.6v-41.5z m404.8 530.2c0 16.7-13.7 30.3-30.6 30.3H355.4c-16.9 0-30.6-13.6-30.6-30.3V382.9h373.6v447.2z"
      fill="#444"
      stroke="#000"
      stroke-width="10"
    /></svg
  >
</div>
