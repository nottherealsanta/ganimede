import { writable, derived } from 'svelte/store';
import { cell_ids } from '../scripts/test_nb';

export const active_cell_id = writable("");

export const active_cell_loc = derived(active_cell_id, ($active_cell_id, set) => {
    const cellLoc = cell_ids.indexOf($active_cell_id);
    set(cellLoc);
}
);
export const is_command_mode = writable(false);

