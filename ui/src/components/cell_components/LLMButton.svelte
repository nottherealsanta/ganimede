<script>
    export let cell;
  
    async function click() {
      console.log("llm button clicked");
    }
  </script>
  
  <div
    class="flex flex-none bg-transparent hover:bg-oli-100 dark:hover:bg-oli-800 active:bg-oli-200 dark:active:bg-oli-700 w-5 h-5 p-0.5 m-0 rounded-sm items-center justify-center fill-oli-800 dark:fill-oli-200 stroke-black dark:stroke-white cursor-pointer pointer-events-auto"
    on:mousedown|stopPropagation={(e) => {
      click();
    }}
  >
    <svg
    viewBox="0 0 64 64"
    stroke-width="3"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g >
      <circle cx="53.63" cy="31.6" r="5.82" />
      <circle cx="26.33" cy="51.651" r="5.82" />
      <circle cx="19.32" cy="16.655" r="5.82" />
      <circle cx="34.51" cy="29.27" r="4.7" />
      <line x1="48.93" y1="34.04" x2="31.446" y2="48.94" style="" />
      <line x1="19.826" y1="20.954" x2="23.728" y2="46.187" style="" />
      <line x1="23.501" y1="19.071" x2="30.754" y2="26.809" style="" />
      <line x1="39.22" y1="29.8" x2="47.81" y2="30.45" />
      <line
        x1="33.206"
        y1="33.401"
        x2="28.012"
        y2="45.66"
        style="transform-origin: 31.439px 38.959px;"
      />
    </g>
  </svg>  
  </div>
  