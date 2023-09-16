# Ganimede

_Rethinking of Computational Notebooks, Jupyter Whiteboard_

```sh
pip install ganimede
```

```sh
ganimede <path_to_notebook.ipynb>
```

> [!WARNING]
> Ganimede is in early development and is not ready for production use.

- Canvas: build the flow of code in 2D space
- AI: With cell outputs in context
- Collaboration: real-time collaboration on the same notebook
- Auto cell commit: every run of a cell is saved / versioned
- Production mirroring: real-time auto converts sets of cells to scripts.

## Demo

[![Watch the video](https://img.youtube.com/vi/osR8aek9AuA/hqdefault.jpg)](https://www.youtube.com/embed/osR8aek9AuA)

## Roadmap

- [x] Canvas
- [x] Code execution
- [x] Markdown
- [x] Tissue Grouping (Headings)
- [ ] Connect to LLMs (OpenAI's GPT3.5, GPT4 in-progress)
- [ ] Real-time collaboration [RTC Demo Sep 23](https://www.youtube.com/embed/nIBj7SI_q5U)
- [ ] Auto format code
- [ ] Store run history of cells
- [ ] Mirror to scripts

## Why?

- Not all things in a notebook makes sense in a sequential order, therefore the canvas is a better representation of the flow of code. This also makes it easier to visualize the order and the dependencies between cells.

- Chat and interact with LLMs to generate code and ideas.

- Real-time collaboration and intiutive git integration is a must for any modern tool.

## Built on top of :

- [jupyter_client](https://github.com/jupyter/jupyter_client)
- [svelte](https://github.com/sveltejs/svelte)
- [Yjs](https://github.com/yjs/yjs)
- [monaco-editor](https://github.com/microsoft/monaco-editor)
- [starlette](https://github.com/encode/starlette)
