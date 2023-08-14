<script>
  export let cell;

  import { delete_cell } from "../../stores/_notebook";

  async function click() {
    delete_cell(cell.id);
  }
</script>

<div
  class="flex flex-none bg-transparent hover:bg-oli-100 dark:hover:bg-oli-800 active:bg-oli-200 dark:active:bg-oli-700 w-5 h-5 p-0.5 m-0 rounded-sm items-center justify-center stroke-black dark:stroke-white cursor-pointer pointer-events-auto"
  on:mousedown|stopPropagation={(e) => {
    click();
  }}
>
  <svg viewBox="0 0 21 21" xmlns="http://www.w3.org/2000/svg" fill="#000000"
    ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
      id="SVGRepo_tracerCarrier"
      stroke-linecap="round"
      stroke-linejoin="round"
    ></g><g id="SVGRepo_iconCarrier">
      <g
        fill="none"
        fill-rule="evenodd"
        stroke-linecap="round"
        stroke-linejoin="round"
        transform="translate(2 3)"
      >
        <path
          d="m1.5 4.5h14v7.9976807c0 1.1045695-.8954305 2-2 2h-10c-1.1045695 0-2-.8954305-2-2zm0-3.9777832h14c.5522847 0 1 .44771525 1 1v1.9777832c0 .55228475-.4477153 1-1 1h-14c-.55228475 0-1-.44771525-1-1v-1.9777832c0-.55228475.44771525-1 1-1z"
        ></path> <path d="m6.5 7.5h4"></path>
      </g>
    </g></svg
  >
</div>
