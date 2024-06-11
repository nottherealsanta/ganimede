<script>
  // @ts-nocheck

  import { onDestroy, onMount } from "svelte";
  import Sortable, { MultiDrag, Swap } from "sortablejs";
  // Svelte Library Variables
  let list;
  let sortable;
  let className;
  /**
   * Classes to be added to the list div
   */
  export { className as class };
  /**
   * Add a multiDrag class. Automatically mounts the multiDrag Plugin, sets it to true and sets fallbackTolerance to 3.
   * @type {string}
   */
  export let multiDragClass = null;
  /**
   * Add a swap class. Automatically mounts the swap Plugin, sets it to true.
   * @type {string}
   */
  export let swapClass = null;
  // Default Options
  /**
   * "name" OR { name: "...", pull: [true, false, 'clone', array], put: [true, false, array] }
   * @type {string | GroupOptions}
   * */
  export let group = undefined;
  /** Sorting inside list */
  export let sort = true;
  /** Disables the sortable if set to true. */
  export let disabled = false;
  export let store = undefined;
  /**
   * Drag handle selector within list items
   * @type {string}
   * */
  export let handle = undefined;
  /** Threshold of the swap zone. Must be between 0 and 1. */
  export let swapThreshold = 1; // 0 <= x <= 1
  /** Will always use inverted swap zone if set to true. */
  export let invertSwap = false;
  /**
   * Threshold of the inverted swap zone (will be set to swapThreshold value by default).
   * @type {number}
   */
  export let invertedSwapThreshold = undefined; // will be set to same as swapThreshold if default
  /** Remove the clone element when it is not showing, rather than just hiding it */
  export let removeCloneOnHide = true;
  /** Class name for the drop placeholder. */
  export let ghostClass = "sortable-ghost";
  /** Class name for the chosen item. */
  export let chosenClass = "sortable-chosen";
  /** Class name for the dragging item. */
  export let dragClass = "sortable-drag";
  /** Elements to ignore */
  export let ignore = "a; img";
  /**
   * Selectors that do not lead to dragging (String or Function)
   * @type {string | Function}
   */
  export let filter = undefined;
  export let preventOnFilter = true;
  export let animation = 0;
  /**
   * Easing for animation. Defaults to null.
   *
   * See https://easings.net/ for examples.
   *
   * For other possible values, see
   * https://www.w3schools.com/cssref/css3_pr_animation-timing-function.asp
   *
   * @type {string | function}
   */
  export let easing = undefined;
  /** HTML attribute that is used by the `toArray()` method. */
  export let dataIdAttr = "data-id";
  /** Time in milliseconds to define when the sorting should start */
  export let delay = 0;
  /** Whether or not the delay should be applied only if the user is using touch (eg. on a mobile device). No delay will be applied in any other case. */
  export let delayOnTouchOnly = false;
  /** Ignore the HTML5 DnD behaviour and force the fallback to kick in */
  export let forceFallback = false;
  /** Class name for the cloned DOM Element when using forceFallback. */
  export let fallbackClass = "sortable-fallback";
  /** Appends the cloned DOM Element into the Document's Body. */
  export let fallbackOnBody = false;
  /** Specify in pixels how far the mouse should move before it's considered as a drag. */
  export let fallbackTolerance = 0;
  export let fallbackOffset = {
    x: 0,
    y: 0,
  };
  /** Pixel distance mouse must be from empty sortable to insert drag element into it */
  export let emptyInsertThreshold = 5;
  /** Direction that the Sortable should sort in. Can be set to 'vertical', 'horizontal', or a function, which will be called whenever a target is dragged over. Must return 'vertical' or 'horizontal'. Leave blank to auto detect.*/
  export let direction = undefined;
  /** How many pixels the point should move before cancelling a delayed drag event */
  export let touchStartThreshold = undefined;
  export let setData = undefined;
  /** Specifies which items inside the element should be draggable. */
  export let draggable = null;
  /**
   * Element is chosen
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onChoose = undefined;
  /**
   * Element is unchosen
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onUnchoose = undefined;
  /**
   * Element dragging started
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onStart = undefined;
  /**
   * Element dragging ended
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onEnd = undefined;
  /**
   * Element is dropped into the list from another list
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onAdd = undefined;
  /**
   * Changed sorting within list
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onUpdate = undefined;
  /**
   * Element is removed from the list into another list
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onRemove = undefined;
  /**
   * Attempt to drag a filtered element
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onFilter = undefined;
  /**
   * Called by any change to the list (add / update / remove)
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onSort = undefined;
  /**
   * Called when creating a clone of element
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onClone = undefined;
  /**
   * Event when you move an item in the list or between lists
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onMove = undefined;
  /**
   * Called when dragging element changes position
   * @type {fn(event: SortableEvent) => void}
   * */
  export let onChange = undefined;
  let options;
  onMount(() => {
    options = {
      group,
      sort,
      disabled,
      store,
      handle,
      swapThreshold,
      invertSwap,
      invertedSwapThreshold,
      removeCloneOnHide,
      ghostClass,
      chosenClass,
      dragClass,
      ignore,
      filter,
      preventOnFilter,
      animation,
      easing,
      dataIdAttr,
      delay,
      delayOnTouchOnly,
      forceFallback,
      fallbackClass,
      fallbackOnBody,
      fallbackTolerance,
      fallbackOffset,
      emptyInsertThreshold,
      direction,
      touchStartThreshold,
      setData,
      onChoose,
      onUnchoose,
      onStart,
      onEnd,
      onAdd,
      onUpdate,
      onRemove,
      onFilter,
      onSort,
      onClone,
      onMove,
      onChange,
    };
    if (draggable) {
      options.draggable = draggable;
    }
    if (multiDragClass) {
      try {
        Sortable.mount(new MultiDrag());
      } catch (e) {
        // BUG: Do nothing. Find a better way to handle multiple mounts.
      }
      options.multiDrag = true;
      options.selectedClass = multiDragClass;
      options.fallbackTolerance = 3;
      options.multiDragKey = "shift";
    }
    if (swapClass) {
      try {
        Sortable.mount(new Swap());
      } catch (e) {
        // BUG: Do nothing. Find a better way to handle multiple mounts.
      }
      options.swap = true;
      options.swapClass = swapClass;
    }
    sortable = Sortable.create(list, { ...options });
  });
  onDestroy(() => {
    if (sortable) sortable.destroy();
  });
</script>

<!--
  @component
  Svelte wrapper for SortableJS.
  
  - Usage:
    ```tsx
    <SortableList>
      <div>List Item 1</div>
      <div>List Item 2</div>
      <div>List Item 3</div>
    </SortableList>
      ```
    -->

<div bind:this={list} class={className}>
  <slot />
</div>
