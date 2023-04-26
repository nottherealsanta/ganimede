export function get_mouse_pos_on_cell(cell, mouse_pos) {
  // check if mouse is inside cell
  if (mouse_pos.x > cell.left - 16 && mouse_pos.x < cell.left + cell.width &&
    mouse_pos.y > cell.top && mouse_pos.y < cell.top + cell.height) {
    return {
      x: mouse_pos.x - cell.left,
      y: mouse_pos.y - cell.top
    };
  } else {
    return null;
  }
}

export function is_mouse_inside_this_div(div, mouse_pos) {
  if (!div) {
    return false;
  }
  const rect = div.getBoundingClientRect();
  return mouse_pos.x > rect.left && mouse_pos.x < rect.right &&
    mouse_pos.y > rect.top && mouse_pos.y < rect.bottom;
}

export function detect_cell_edge(cell, mouse_pos_on_cell, edge_size = 5) {

  if (!mouse_pos_on_cell) {
    return null;
  }

  const pad = 1;
  const x = mouse_pos_on_cell.x - pad;
  const y = mouse_pos_on_cell.y - pad;
  const width = cell.width - 2 * pad;
  const height = cell.height - 2 * pad;

  // if outside cell bounds, return null
  if (x < 0 || x > width || y < 0 || y > height) {
    return null;
  }

  if (x < edge_size && y < edge_size) {
    return "top-left";
  } else if (x > width - edge_size && y < edge_size) {
    return "top-right";
  } else if (x < edge_size && y > height - edge_size) {
    return "bottom-left";
  } else if (x > width - edge_size && y > height - edge_size) {
    return "bottom-right";
  } else if (x < edge_size) {
    return "left";
  } else if (x > width - edge_size) {
    return "right";
  } else if (y < edge_size) {
    return "top";
  } else if (y > height - edge_size) {
    return "bottom";
  }
}

export function cell_edge_to_cursor(edge) {
  if (edge === "top-left" || edge === "bottom-right") {
    return "nwse-resize";
  } else if (edge === "top-right" || edge === "bottom-left") {
    return "nesw-resize";
  } else if (edge === "left" || edge === "right") {
    return "ew-resize";
  } else if (edge === "top" || edge === "bottom") {
    return "ns-resize";
  }
}

export function cell_edge_to_resize_fn(mouse_pos, clicked, cell) {

  if (clicked.at === "top") {
    cell.height = cell.height + (cell.top - mouse_pos.y);
    cell.top = mouse_pos.y;
  } else if (clicked.at === "bottom") {
    cell.height = mouse_pos.y - cell.top;
  } else if (clicked.at === "left") {
    cell.width = cell.width + (cell.left - mouse_pos.x);
    cell.left = mouse_pos.x;
  } else if (clicked.at === "right") {
    cell.width = mouse_pos.x - cell.left + 4;
  } else if (clicked.at === "top-left") {
    cell.height = cell.height + (cell.top - mouse_pos.y);
    cell.top = mouse_pos.y;
    cell.width = cell.width + (cell.left - mouse_pos.x);
    cell.left = mouse_pos.x;
  } else if (clicked.at === "top-right") {
    cell.height = cell.height + (cell.top - mouse_pos.y);
    cell.top = mouse_pos.y;
    cell.width = mouse_pos.x - cell.left;
  } else if (clicked.at === "bottom-left") {
    cell.height = mouse_pos.y - cell.top;
    cell.width = cell.width + (cell.left - mouse_pos.x);
    cell.left = mouse_pos.x;
    console.log(cell.height, cell.width, cell.top, cell.left)
  } else if (clicked.at === "bottom-right") {
    cell.height = mouse_pos.y - cell.top;
    cell.width = mouse_pos.x - cell.left;
  }

  return [cell.top, cell.left, cell.height, cell.width];
}
