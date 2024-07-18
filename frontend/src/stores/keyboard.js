import { get } from 'svelte/store';
import { is_command_mode, active_cell_id, active_cell_loc, ycells, undoManager, queue_cell, create_cell, ydoc } from './notebook';

function move_to_prev_cell() {
  let x = get(active_cell_loc);
  if (x > 0) {
    active_cell_id.set(ycells.get(x - 1));
  }
}
function move_to_next_cell() {
  let x = get(active_cell_loc);
  if (x < ycells.length - 1) {
    active_cell_id.set(ycells.get(x + 1));
  }
}

function create_cell_below() {
  let active_cell_type = ydoc.getMap(get(active_cell_id)).get('type');
  console.log(active_cell_type);
  create_cell(get(active_cell_loc) + 1, active_cell_type);
}
function create_cell_above() {
  let active_cell_type = ydoc.getMap(get(active_cell_id)).get('type');
  create_cell(get(active_cell_loc), active_cell_type);
}

export const keydown_function = (event) => {
  // Check if the Escape key is pressed to enter command mode
  if (event.key === 'Escape') {

    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur()
    }
    is_command_mode.set(true);
  } else if (get(is_command_mode)) {
    if (event.key === 'ArrowUp') {
      // move active cell to the previous cell
      // TODO: account for collapsed cells
      event.preventDefault();

      move_to_prev_cell();

    }
    else if (event.key === 'ArrowDown') {
      // move active cell to the next cell

      event.preventDefault();

      move_to_next_cell();
    }
    else if (event.key === 'Enter') {
      event.preventDefault();

      // if shift is pressed, queue cell and move to next cell
      if (event.shiftKey) {
        queue_cell(get(active_cell_id));

        // if last cell, create cell below
        if (get(active_cell_loc) === ycells.length - 1) {
          create_cell_below();
        }
        else {
          move_to_next_cell();
        }
      }
      // if ctrl is pressed, queue cell
      else if (event.ctrlKey) {
        queue_cell(get(active_cell_id));
      }
      // if neither shift nor ctrl is pressed, edit cell
      else {
        is_command_mode.set(false);
      }
    }
    else if (event.key === 'a') {
      create_cell_above();
    }
    else if (event.key === 'b') {
      create_cell_below();
    }
    else if (event.key === 'x') {
      // Logic to cut the selected cell
    }
    else if (event.key === 'c') {
      // Logic to copy the selected cell
    }
    else if (event.key === 'v') {
      // Logic to paste the cell below
    }
    else if (event.key === 'd' && event.repeat) {
      // Logic to delete the selected cell (press D twice)

    }
    else if (event.key === 'z') {
      // Logic to undo cell deletion
      undoManager.undo();
    }
    else if (event.key === 'y') {
      // Logic to change the cell type to Code
    }
    else if (event.key === 'm') {
      // Logic to change the cell type to Markdown
    }

  }

}