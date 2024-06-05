import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
// import monacoEditorPlugin from 'vite-plugin-monaco-editor';


export default defineConfig({
    plugins: [
        svelte(),
        // new monacoEditorPlugin.default({
        //     languageWorkers: ['json', 'editorWorkerService']

        // })
    ],
    build: {
        outDir: '../api/ganimede/ui_dist/'
    }
});