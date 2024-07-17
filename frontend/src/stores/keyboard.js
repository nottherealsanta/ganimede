import { get } from 'svelte/store';
import { is_command_mode, active_cell_id, active_cell_loc, ycells, undoManager, queue_cell } from './notebook';

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

export const keydown_function = (event) => {
  // if (["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].indexOf(event.code) > -1) {
  //   event.preventDefault();
  // }
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
        move_to_next_cell();
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
      // Logic to insert a cell above

      // TODO: Implement the logic to insert a cell above
    }
    else if (event.key === 'b') {
      // Logic to insert a cell below
      // TODO: Implement the logic to insert a cell below
    }
    else if (event.key === 'x') {
      // Logic to cut the selected cell
      // TODO: Implement the logic to cut the selected cell
    }
    else if (event.key === 'c') {
      // Logic to copy the selected cell
      // TODO: Implement the logic to copy the selected cell
    }
    else if (event.key === 'v') {
      // Logic to paste the cell below
      // TODO: Implement the logic to paste the cell below
    }
    else if (event.key === 'd' && event.repeat) {
      // Logic to delete the selected cell (press D twice)
      // TODO: Implement the logic to delete the selected cell

    }
    else if (event.key === 'z') {
      // Logic to undo cell deletion
      // TODO: Implement the logic to undo cell deletion
      undoManager.undo();
    }
    else if (event.key === 'y') {
      // Logic to change the cell type to Code
      // TODO: Implement the logic to change the cell type to Code
    }
    else if (event.key === 'm') {
      // Logic to change the cell type to Markdown
      // TODO: Implement the logic to change the cell type to Markdown
    }

  }

}