import { derived, writable } from "svelte/store";

function createNotebookStore() {
    const { subscribe, set, update } = writable({});

    return {
        subscribe,
        set,
        update,
        async get() {
            const response = await fetch("/notebook");
            const data = await response.json();
            set(JSON.parse(JSON.stringify(data)));
        },

    };
}

export let notebook = createNotebookStore();

export const cells = derived(notebook, $notebook => $notebook.cells);
cells.set = (value) => notebook.update(n => {
    n.cells = value;
    return n;
});

export const id_map = derived(notebook, $notebook => {
    if ($notebook["metadata"] !== undefined) {
        return $notebook["metadata"]["gm"]["id_map"];
    } else {
        return {};
    }
}
);
id_map.set = (value) => notebook.update(n => {
    n["metadata"]["gm"]["id_map"] = value;
    return n;
});
