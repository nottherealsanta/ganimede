<script>
  export let x = 0;
  export let y = 0;
  export let id = "";
  export let color = "";
</script>

<div
  class="m-0 p-0"
  style="position: absolute; top: {y}px; left: {x}px; z-index: 99999;"
>
  <svg
    version="1.1"
    id="Layer_1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    x="0px"
    y="0px"
    viewBox="8 5 18 18"
    width="15px"
    height="15px"
  >
    <polygon
      fill={color}
      points="8.2,20.9 8.2,4.9 19.8,16.5 13,16.5 12.6,16.6 "
    />
    <polygon fill={color} points="17.3,21.6 13.7,23.1 9,12 12.7,10.5 " />
    <rect
      x="12.5"
      y="13.6"
      transform="matrix(0.9221 -0.3871 0.3871 0.9221 -5.7605 6.5909)"
      width="2"
      height="8"
      fill={color}
    />
    <polygon
      fill={color}
      points="9.2,7.3 9.2,18.5 12.2,15.6 12.6,15.5 17.4,15.5 "
    />
  </svg>

  <div>{id}</div>
</div>
