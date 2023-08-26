# Ganimede

_Rethinking of Computational Notebooks_

```sh
pip install ganimede
```

```sh
ganimede <path_to_notebook.ipynb>
```

> [!WARNING]
> Ganimede is in early development and is not ready for production use.

- Canvas: build the flow of code in 2D space
- Collaboration: real-time collaboration on the same notebook
- Auto cell commit: every run of a cell is saved / versioned
- Production mirroring: real-time auto converts sets of cells to scripts.

### Demo

[![Watch the video](https://img.youtube.com/vi/osR8aek9AuA/hqdefault.jpg)](https://www.youtube.com/embed/osR8aek9AuA)

### Roadmap

- Real-time collaboration
- Store run history of cells
- Easy to visualize execution order
- Mirror to scripts
- Auto format code

### Why?

- Not all things in a notebook makes sense in a sequential order, therefore the canvas is a better representation of the flow of code. This also makes it easier to visualize the order and the dependencies between cells.

- Data science workflows are constantly switching between working in a notebook and converting it to scripts. This is exaggerated when working on a project that is already in production. This also decreases team efficiency.

- Real-time collaboration and intiutive git integration is a must for any modern tool.

### Built on top of :

- [jupyter_client](https://github.com/jupyter/jupyter_client)
- [svelte](https://github.com/sveltejs/svelte)
- [Yjs](https://github.com/yjs/yjs)
- [monaco-editor](https://github.com/microsoft/monaco-editor)
- [starlette](https://github.com/encode/starlette)
