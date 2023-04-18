export function detect_cell_edge(cell, mouse_pos, edge_size = 5) {

    const pad = 1;
    const x = mouse_pos.x - cell.left - pad;
    const y = mouse_pos.y - cell.top - pad;
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
    } else {
        return "inside";
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
    } else if (edge === "inside") {
        return "move";
    } else {
        console.error("Invalid edge", edge);
    }
}

export function cell_edge_to_resize_fn(mouse_pos, clicked, cell) {

    if (clicked.at === "inside") {
        cell.top = mouse_pos.y - clicked.y;
        cell.left = mouse_pos.x - clicked.x;
    } else if (clicked.at === "top") {
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
    } else {
        console.error("Invalid edge", clicked.at);
    }

    return [cell.top, cell.left, cell.height, cell.width];
}