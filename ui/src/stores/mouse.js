import { readable, get, writable } from 'svelte/store';

import { zoom } from './zoom.js';

export default readable({ x: 0, y: 0 }, (set) => {
	document.body.addEventListener("mousemove", move);

	function move(event) {

		set({
			x: Math.floor(event.clientX / get(zoom) + window.scrollX / get(zoom)),
			y: Math.floor(event.clientY / get(zoom) + window.scrollY / get(zoom))
			// x: Math.floor(event.clientX + window.scrollX),
			// y: Math.floor(event.clientY + window.scrollY)
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

// current cell that mouse is over
export const mouse_on_cell = readable(null, (set) => {
	document.body.addEventListener('mousemove', move);

	function move(event) {
		const elements = document.elementsFromPoint(event.clientX, event.clientY);
		const cells = elements.filter((el) => el.classList.contains('cell'));
		const tissues = elements.filter((el) => el.classList.contains('tissue'));
		const dropzones = elements.filter((el) => el.id === 'dropzone');

		let top_tissue_id = tissues.length > 0 ? tissues[0].getAttribute('cell_id') : null;

		if (top_tissue_id) {
			// check if id not in dropzones
			if (dropzones.length > 0) {
				if (dropzones[0].getAttribute('cell_id') !== top_tissue_id) {
					return set(tissues[0]);
				} else {
					// log cell_id from cells
					if (cells.length === 2) {
						return set(cells[1]);
					} else if (cells.length === 1) {
						return set(cells[0]);
					} else {
						return set(null);
					}
				}
			}
		}



	}

	return () => {
		document.body.removeEventListener('mousemove', move);
	};
});


export const dragging_cell_id = writable(null);