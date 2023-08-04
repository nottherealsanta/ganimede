
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
import mouse_pos from "./mouse";

export let zoom = writable(1);
const d_zoom = 0.025;
const max_zoom = 1.7;
const min_zoom = 0.25;

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

export function zoom_in() {
    zoom.update((z) => {
        z += 0.15;
        if (z > max_zoom) {
            z = max_zoom;
        } else {
            // window.scrollBy({
            //     left: -window.innerWidth * d_zoom,
            //     top: -window.innerHeight * d_zoom,
            //     behavior: "instant",
            // });
        }
        console.log(window.scrollX, window.scrollY)
        return z;
    });
}
export function zoom_out() {
    zoom.update((z) => {
        z -= 0.15;
        if (z < min_zoom) {
            z = min_zoom;
        } else {
            // window.scrollBy({
            //     left: window.innerWidth * d_zoom,
            //     top: window.innerHeight * d_zoom,
            //     behavior: "instant",
            // });
        }
        return z;
    });
}
