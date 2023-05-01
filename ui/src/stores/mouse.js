import { readable, get } from 'svelte/store';

import { zoom } from './zoom.js';

export default readable({ x: 0, y: 0 }, (set) => {
	document.body.addEventListener("mousemove", move);

	function move(event) {

		set({
			x: Math.floor(event.clientX / get(zoom) + window.scrollX / get(zoom)),
			y: Math.floor(event.clientY / get(zoom) + window.scrollY / get(zoom))
		});
	}

	return () => {
		document.body.removeEventListener("mousemove", move);
	}
})