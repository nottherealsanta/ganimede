import { get } from 'svelte/store';
import { is_command_mode, active_cell_id, active_cell_loc, cell_ids } from './notebook';

export const keydown_function = (event) => {
  // if (["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].indexOf(event.code) > -1) {
  //   event.preventDefault();
  // }
  // Check if the Escape key is pressed to enter command mode
  if (event.key === 'Escape') {
    console.log('Escape');
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur()
    }
    is_command_mode.set(true);
  } else if (get(is_command_mode)) {
    // Check if the ArrowUp key is pressed to move to the previous cell
    if (event.key === 'ArrowUp') {
      // move active cell to the previous cell
      console.log('ArrowUp');
      event.preventDefault();
      let x = get(active_cell_loc);
      if (x > 0) {
        active_cell_id.set(get(cell_ids)[x - 1]);
      }
    }
    // Check if the ArrowDown key is pressed to move to the next cell
    else if (event.key === 'ArrowDown') {
      // move active cell to the next cell
      console.log('ArrowDown');
      event.preventDefault();
      let x = get(active_cell_loc);
      if (x < get(cell_ids).length - 1) {
        active_cell_id.set(get(cell_ids)[x + 1]);
      }
    }
    // Check if the Enter key is pressed to enter edit mode
    else if (event.key === 'Enter') {
      console.log('Enter');
      event.preventDefault();
      is_command_mode.set(false);
    }
    // Additional shortcuts for command mode
    else if (event.key === 'a') {
      // Logic to insert a cell above
      console.log('a');
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
      console.log('dd');
    }
    else if (event.key === 'z') {
      // Logic to undo cell deletion
      // TODO: Implement the logic to undo cell deletion
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