import { readable, get, writable } from 'svelte/store';

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

// stack of tissue that mouse is over

export const mouse_on_tissues = readable([], (set) => {
	document.body.addEventListener('mousemove', move);

	function move(event) {
		const elements = document.elementsFromPoint(event.clientX, event.clientY);
		const tissues = elements.filter((el) => el.classList.contains('tissue'));
		// const cellIds = tissues.map((tissue) => tissue.getAttribute('cell_id'));

		set(tissues);
	}

	return () => {
		document.body.removeEventListener('mousemove', move);
	};
});

export const dragging_cell_id = writable(null);