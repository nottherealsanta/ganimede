import { writable, derived } from 'svelte/store';
import { cell_ids as nb_cell_ids, cell_maps } from '../scripts/test_nb';

export const cell_ids = writable(nb_cell_ids);

export const active_cell_id = writable("");

export const active_cell_loc = derived(active_cell_id, ($active_cell_id, set) => {
    const cellLoc = nb_cell_ids.indexOf($active_cell_id);
    set(cellLoc);
}
);
export const is_command_mode = writable(true);

class CellStore {
    constructor(cellData) {
        this.id = cellData.id;
        this.type = cellData.type;
        this.source = cellData.source;
        this.execution_count = cellData.execution_count;
        this.outputs = cellData.outputs;
        this.collapsed = cellData.collapsed;
        this.parent_collapsed = cellData.parent_collapsed;
        this.state = cellData.state;
        this.execution_time = cellData.execution_time;

        this.is_hover = writable(false);
        this.is_active = writable(false);
        this.is_focus = writable(false);

        this.heading_level = derived(
            [this],
            ([$cell]) => {
                if ($cell.type === 'markdown') {
                    const headingMatch = $cell.source[0].match(/^(#+)\s/);
                    return headingMatch ? headingMatch[1].length : null;
                }
                return null;
            }
        );

        this.is_markdown = derived(
            [this],
            ([$cell]) => $cell.type === 'markdown'
        );
    }

    subscribe(run) {
        return derived(
            [
                this.is_hover,
                this.is_active,
                this.is_focus,
                this.heading_level,
                this.is_markdown
            ],
            () => this
        ).subscribe(run);
    }

    setHover(value) {
        this.is_hover.set(value);
    }

    setActive(value) {
        this.is_active.set(value);
    }

    setFocus(value) {
        this.is_focus.set(value);
    }
}

function createCellStore(cellData) {
    return new CellStore(cellData);
}

export let cell_stores = {};
nb_cell_ids.forEach((cell_id) => {
    cell_stores[cell_id] = createCellStore(cell_maps[cell_id]);
});