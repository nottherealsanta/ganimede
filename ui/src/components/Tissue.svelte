<script>
  import { onMount } from "svelte";

  export let cell_id;
  let cell_div;

  import {
    cp_graph,
    html_elements,
    ydoc,
    pc_graph,
    ypc_graph,
    move_cell,
  } from "../stores/_notebook";

  onMount(() => {
    cell_div.setAttribute("cell_id", cell_id);
    $html_elements[cell_id] = cell_div;
    $html_elements[cell_id].setAttribute("dragging", "false");
  });

  let cell = {
    // cell should have dragging, while dragging all yjs' undomanager stops capturing changes
    ycell: ydoc.getMap(cell_id),

    get id() {
      return this.ycell.get("id");
    },
    get type() {
      return this.ycell.get("type");
    },
    get source() {
      return this.ycell.get("source");
    },
    get execution_count() {
      return this.ycell.get("execution_count");
    },
    get outputs() {
      return this.ycell.get("outputs");
    },
    get top() {
      return this.ycell.get("top");
    },
    get left() {
      return this.ycell.get("left");
    },
    get width() {
      return this.ycell.get("width");
    },
    get height() {
      return this.ycell.get("height");
    },
    get collapsed() {
      return this.ycell.get("collapsed");
    },
    get state() {
      return this.ycell.get("state");
    },

    set id(value) {
      console.error("ID is read-only");
    },
    set type(value) {
      this.ycell.set("type", value);
    },
    set source(value) {
      this.ycell.set("source", value);
    },
    set execution_count(value) {
      console.error("Execution count is read-only");
    },
    set outputs(value) {
      console.error("Outputs is read-only");
    },
    set top(value) {
      this.ycell.set("top", value);
    },
    set left(value) {
      this.ycell.set("left", value);
    },
    set width(value) {
      this.ycell.set("width", value);
    },
    set height(value) {
      this.ycell.set("height", value);
    },
    set collapsed(value) {
      this.ycell.set("collapsed", value);
    },
    set state(value) {
      console.error("State is read-only");
    },
  };

  cell.ycell.observe((yevent) => {
    cell = cell; // force reactivity
  });

  import CodeCell from "./CodeCell.svelte";
  import MarkdownCell from "./MarkdownCell.svelte";

  function get_cell(id) {
    return ydoc.getMap(id).toJSON();
  }

  // dragging
  import mouse_pos from "../stores/mouse.js";

  let dragging = false;
  let dragging_began = false;
  let dh_clicked = {
    x: 0,
    y: 0,
  };
  let drag_cell_pos = {
    x: null,
    y: null,
  };

  let selected_dragzone = null;
  let dragover_cell = null;
  let draggedOverElements = [];

  function drag_mousedown(e) {
    if (e.button === 0) {
      e.stopPropagation();
      e.preventDefault();
      dragging = true;
      dragging_began = false;
      dh_clicked = {
        x: $mouse_pos.x - cell.left,
        y: $mouse_pos.y - cell.top,
      };
      drag_cell_pos = {
        x: cell.left,
        y: cell.top,
      };
      $html_elements[cell_id].setAttribute("dragging", "true");
    }
  }
  function drag_mousemove(e) {
    if (dragging) {
      dragging_began = true;
      e.preventDefault();
      e.stopPropagation();

      // set cell position while dragging
      drag_cell_pos = {
        x: $mouse_pos.x - dh_clicked.x,
        y: $mouse_pos.y - dh_clicked.y,
      };

      cell.top = $mouse_pos.y - dh_clicked.y;
      cell.left = $mouse_pos.x - dh_clicked.x;

      // top of
      const elements_under = document.elementsFromPoint(e.clientX, e.clientY);
      let cell_under = elements_under.filter(
        (el) =>
          el.classList.contains("cell") &&
          el.getAttribute("cell_id") !== cell_id,
      )[0];
      let tissue_under = elements_under.filter(
        (el) =>
          el.classList.contains("tissue") &&
          el.getAttribute("cell_id") !== cell_id,
      )[0];
      const dragzone_under = elements_under.filter((el) =>
        el.classList.contains("dropzone"),
      )[0];
      const dragzone_under_tissue = dragzone_under
        ? dragzone_under.parentNode
        : undefined;

      // if elements_under has dragzone that's cellid = cell_id
      if (cell_under == undefined && tissue_under !== undefined) {
        if (
          (dragzone_under !== undefined &&
            dragzone_under.getAttribute("cell_id") !==
              tissue_under.getAttribute("cell_id")) ||
          dragzone_under == undefined
        ) {
          if (tissue_under.getAttribute("cell_id") !== cell_id) {
            cell_under = tissue_under;
          }
        }
      }

      // when moving fast, the tissue might want to be next to it's children
      if (cell_under !== undefined) {
        if (
          $pc_graph[cell_id] &&
          $pc_graph[cell_id].includes(cell_under.getAttribute("cell_id"))
        ) {
          cell_under = undefined;
        }
      }

      // check if on cell
      if (cell_under) {
        dragover_cell = cell_under;
        let _bounding_rect = {
          top: cell_under.offsetTop - 4,
          left: cell_under.offsetLeft,
          width: cell_under.getBoundingClientRect().width,
          height: cell_under.getBoundingClientRect().height,
          bottom:
            cell_under.offsetTop +
            cell_under.getBoundingClientRect().height +
            4,
        };
        // if mouse is on bottom/top half of cell
        if (dragover_cell) {
          if ($mouse_pos.y > _bounding_rect.top + _bounding_rect.height / 2) {
            // draw pointer on bottom
            dragover_cell.style.borderTop = "";
            dragover_cell.style.borderBottom = "3px solid #FF9F3C";
            dragover_cell.setAttribute("position", "bottom");
          } else {
            // draw pointer on top
            dragover_cell.style.borderTop = "3px solid #FF9F3C";
            dragover_cell.style.borderBottom = "";
            dragover_cell.setAttribute("position", "top");
          }
        }

        // remove draggedOverElements border except for dragover_cell
        draggedOverElements.forEach((el) => {
          if (el !== dragover_cell) {
            el.style.borderTop = "";
            el.style.borderBottom = "";
          }
        });

        // if moved to another cell
        if (
          dragover_cell &&
          dragover_cell.getAttribute("cell_id") !==
            cell_under.getAttribute("cell_id")
        ) {
          dragover_cell.style.borderTop = "";
          dragover_cell.style.borderBottom = "";
          dragover_cell = null;
        }
      }

      // if mouse_on_cell is null
      if (cell_under === undefined && dragover_cell) {
        dragover_cell.style.borderTop = "";
        dragover_cell.style.borderBottom = "";
        dragover_cell = null;
      }

      // check if on tissue
      if (
        dragzone_under &&
        dragzone_under_tissue.getAttribute("cell_id") !== cell_id
      ) {
        // if moved to another tissue
        if (
          selected_dragzone &&
          selected_dragzone.getAttribute("cell_id") !== cell_id
        ) {
          selected_dragzone.classList.remove("ring-1");
        }
        // set styles
        dragzone_under.classList.add("ring-1");
        dragzone_under.classList.add("ring-orange-300");
        selected_dragzone = dragzone_under;
      } else if (dragzone_under === undefined) {
        if (selected_dragzone) {
          selected_dragzone.classList.remove("ring-1");
          selected_dragzone = null;
        }
      }
    }
  }
  function drag_mouseup(e) {
    if (dragging && dragging_began) {
      dh_clicked = {
        x: 0,
        y: 0,
      };

      cell.top = drag_cell_pos.y;
      cell.left = drag_cell_pos.x;

      drag_cell_pos = {
        x: null,
        y: null,
      };

      move_cell(cell_id, dragover_cell, selected_dragzone);

      if (dragover_cell) {
        dragover_cell.style.borderTop = "";
        dragover_cell.style.borderBottom = "";
        dragover_cell = null;
      }
      if (selected_dragzone) {
        selected_dragzone.classList.remove("ring-1");
      }
      draggedOverElements = [];
    }
    dragging_began = false;
    dragging = false;
    $html_elements[cell_id].setAttribute("dragging", "false");
  }

  // ---------- Parent and previous cell

  let yparent_cell;
  $: if ($cp_graph[cell_id]) {
    yparent_cell = ydoc.getMap($cp_graph[cell_id]);
  }
  let parent_cell;
  $: if (yparent_cell) {
    parent_cell = yparent_cell.toJSON();
    yparent_cell.observe((yevent) => {
      parent_cell = yparent_cell.toJSON();
    });
  }

  let yprev_cell;
  $: if ($cp_graph[cell_id]) {
    yprev_cell = ydoc.getMap(
      ypc_graph.get($cp_graph[cell_id]).toJSON()[
        ypc_graph.get($cp_graph[cell_id]).toJSON().indexOf(cell_id) - 1
      ],
    );
  }
  let prev_cell;
  $: if (yprev_cell) {
    prev_cell = yprev_cell.toJSON();
    yprev_cell.observe((yevent) => {
      prev_cell = yprev_cell.toJSON();
    });
  }

  $: if (
    $cp_graph[cell_id] &&
    !dragging &&
    $html_elements[$cp_graph[cell_id]]
  ) {
    let cell_list_loc = ypc_graph
      .get($cp_graph[cell_id])
      .toJSON()
      .indexOf(cell_id);
    if (cell_list_loc === 0) {
      let top_pos =
        parent_cell.top +
        $html_elements[$cp_graph[cell_id]].querySelector("#title")
          .clientHeight +
        32;
      let left_pos = parent_cell.left + 8;
      if (cell.top !== top_pos) {
        cell.top = top_pos;
      }
      if (cell.left !== left_pos) {
        cell.left = left_pos;
      }
    } else {
      let prev_cell_id = ypc_graph.get($cp_graph[cell_id]).toJSON()[
        cell_list_loc - 1
      ];
      if ($html_elements[prev_cell_id]) {
        if ($html_elements[prev_cell_id].getAttribute("dragging") === "false") {
          let top_pos = prev_cell.top + prev_cell.height + 11;

          if (cell.top !== top_pos) {
            cell.top = top_pos;
          }
          if (cell.left !== prev_cell.left) {
            cell.left = prev_cell.left;
          }
        }
      }
    }
  }

  // ---------- reactive width and height
  // TODO: This should be from html_element
  let children_w_h = {};
  if ($pc_graph[cell_id]) {
    $pc_graph[cell_id]
      .map((child_cell_id) => {
        return ydoc.getMap(child_cell_id);
      })
      .map((ychild) => {
        return ychild.observe((yevent) => {
          children_w_h[ychild.get("id")] = {
            width: ychild.get("width"),
            height: ychild.get("height"),
          };
        });
      });
  }
  $: if ($pc_graph[cell_id]) {
    // keep only the children that are in $pc_graph
    children_w_h = Object.keys(children_w_h)
      .filter((child_id) => {
        return $pc_graph[cell_id].includes(child_id);
      })
      .reduce((obj, key) => {
        obj[key] = children_w_h[key];
        return obj;
      }, {});
  }

  $: if (ypc_graph.get(cell_id)) {
    ypc_graph.get(cell_id).observe((yevent) => {
      ypc_graph
        .get(cell_id)
        .toJSON()
        .map((child_cell_id) => {
          return ydoc.getMap(child_cell_id);
        })
        .map((ychild) => {
          return ychild.observe((yevent) => {
            children_w_h[ychild.get("id")] = {
              width: ychild.get("width"),
              height: ychild.get("height"),
            };
          });
        });
    });
  }

  $: dropzone_height = children_w_h
    ? Object.values(children_w_h).reduce((acc, child) => {
        return acc + child.height + 11;
      }, 0) + 10
    : 0;
  $: dropzone_width = children_w_h
    ? Object.values(children_w_h).reduce((acc, child) => {
        return Math.max(acc, child.width + 20);
      }, 0)
    : 0;

  // ---------- reactive z-index
  $: if (cell_div) {
    if (!$cp_graph[cell_id]) {
      cell_div.style.zIndex = 1;
    } else {
      cell_div.style.zIndex =
        $html_elements[$cp_graph[cell_id]].style.zIndex + 1;
    }
  }

  // ---------- Components
  import NewCellToolbar from "../components/cell_components/new_cell_toolbar_components/NewCellToolbar.svelte";
  import TissueToolbar from "./cell_components/TissueToolbar.svelte";

  let is_hover = false;
</script>

<div
  class="tissue rounded-r rounded-tl bg-transparent border-2 border-l-[2px] border-oli-100 dark:border-oli-600 ring-sky-400/50 dark:ring-sky-600/50 absolute w-fit h-fit flex flex-col overflow-visible
  {dragging ? 'drop-shadow-2xl dark:drop-shadow-2xl-dark' : ''}
  {!$cp_graph[cell_id] ? 'drop-shadow-lg dark:drop-shadow-lg-dark' : ''}
  {is_hover ? 'ring-1 ' : ''}
  {dragging ? 'ring-4 ' : ''}
  "
  bind:this={cell_div}
  style="
        top: {drag_cell_pos.y ? drag_cell_pos.y : cell.top}px;
        left: {drag_cell_pos.x ? drag_cell_pos.x : cell.left}px;
        cursor: {dragging ? 'grabbing' : 'default'};
        opacity: {dragging ? '0.5' : '1'};
        "
  bind:clientHeight={cell.height}
  bind:clientWidth={cell.width}
  on:mouseenter={() => {
    is_hover = true;
  }}
  on:mouseleave={() => {
    is_hover = false;
  }}
>
  <TissueToolbar
    {cell}
    {is_hover}
    on:mousedown={drag_mousedown}
    on:mouseup={drag_mouseup}
  />

  <!-- title -->
  <div class="bg-oli dark:bg-oli-800 pb-1 h-fit w-full flex" id="title">
    {#if cell.type === "code"}
      <CodeCell {cell} />
    {:else if cell.type === "markdown"}
      <MarkdownCell {cell} />
    {/if}
  </div>

  <!-- <NewCellToolbar {cell_id} /> -->

  <!-- dropzone -->
  <div
    class="dropzone min-h-[25px] rounded-br bg-oli-25 dark:bg-oli-850 border-t border-oli-50 dark:border-oli-700"
    {cell_id}
  >
    <div
      class=" bg-transparent pointer-events-none"
      style="width:{dropzone_width}px; height:{dropzone_height}px;"
      {cell_id}
      on:mousedown={(event) => {
        event.stopPropagation();
      }}
    />
  </div>
  <NewCellToolbar {cell} cell_hover={is_hover} />
  <!-- debug -->
  <!-- <div
    class="absolute -bottom-2 z-[9999] right-0 w-fit h-fit text-gray-500 text-[9px] dark:text-gray-400"
    style="pointer-events: none;"
  >
    {cell_id}
    {cell.top}, {cell.left}
    {#if $html_elements[cell_id]}
      {$html_elements[cell_id].clientWidth} x
      {$html_elements[cell_id].clientHeight}
    {/if}
    {dragging}
  </div> -->
</div>

<svelte:window on:mousemove={drag_mousemove} on:mouseup={drag_mouseup} />
