import { writable, derived } from 'svelte/store';
import { cell_ids as nb_cell_ids } from '../scripts/test_nb';

export const cell_ids = writable(nb_cell_ids);

export const active_cell_id = writable("");

export const active_cell_loc = derived(active_cell_id, ($active_cell_id, set) => {
    const cellLoc = nb_cell_ids.indexOf($active_cell_id);
    set(cellLoc);
}
);
export const is_command_mode = writable(true);

