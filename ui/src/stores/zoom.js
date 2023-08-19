
// import writeable from 'svelte-store/writeable';

// export let zoom = writeable(1);

// window.addEventListener('wheel', (e) => {
//     if (e.ctrlKey || e.metaKey) {
//         e.preventDefault();
//         zoom += e.deltaY * -0.01;
//         document.body.style.transform = `scale(${zoom})`;
//     }
// });

import { writable, get } from "svelte/store";
import mouse_pos from "./mouse.js";

export let zoom = writable(1);
const d_zoom = 0.025;
const max_zoom = 1.65;
const min_zoom = 0.3;

export function set_zoom(e) {
    if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        e.stopImmediatePropagation();

        zoom.update((z) => {
            z -= Math.sign(e.deltaY) * d_zoom;
            z = Math.round(z * 1000) / 1000; // avoids snapping at min and max zoom
            // clip zoom
            if (z < min_zoom) {
                z = min_zoom;
            } else if (z > max_zoom) {
                z = max_zoom;
            } else {
                // zoom in/out
                let _mouse_pos = get(mouse_pos);
                if (_mouse_pos.x !== 0 && _mouse_pos.y !== 0) {
                    window.scrollBy({
                        left: -_mouse_pos.x * d_zoom * Math.sign(e.deltaY),
                        top: -_mouse_pos.y * d_zoom * Math.sign(e.deltaY),
                        behavior: "instant",
                    });
                }
            }
            return z;
        });
    }
}

let scroll_x = 0;
let scroll_y = 0;

let view_width = 0;
let view_height = 0;

let center_x = 0;
let center_y = 0;

document.addEventListener("scroll", () => {
    scroll_x = window.scrollX / get(zoom);
    scroll_y = window.scrollY / get(zoom);
    view_width = window.innerWidth / get(zoom);
    view_height = window.innerHeight / get(zoom);

    center_x = scroll_x + view_width / 2;
    center_y = scroll_y + view_height / 2;
});



export function zoom_in() {
    zoom.update((z) => {
        const new_z = Math.round((z + 0.15) * 100) / 100;
        if (new_z < max_zoom) {
            z = new_z;
            window.scrollBy({
                left: center_x * (0.15),
                top: center_y * (0.15),
                behavior: "instant",
            });
        }
        return z;
    });
}
export function zoom_out() {
    zoom.update((z) => {
        const new_z = Math.round((z - 0.15) * 100) / 100;
        if (new_z > min_zoom) {
            z = new_z;
            window.scrollBy({
                left: -center_x * (0.15),
                top: -center_y * (0.15),
                behavior: "instant",
            });
        }
        return z;
    });
}
