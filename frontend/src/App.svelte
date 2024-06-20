<script>
  import NavBar from "./components/app_components/NavBar.svelte";
  import StatusBar from "./components/app_components/StatusBar.svelte";
  import SideBar from "./components/app_components/SideBar.svelte";
  import Notebook from "./components/nb_components/Notebook.svelte";

  import { onMount } from "svelte";
  import { keydown_function } from "./stores/keyboard";

  onMount(() => {
    window.addEventListener("keydown", keydown_function);
    return () => {
      window.removeEventListener("keydown", keydown_function);
    };
  });
</script>

<div class="app">
  <div class="sidebar-and-nb">
    <SideBar />
    <Notebook />
  </div>
  <StatusBar />
  <NavBar />
</div>

<style>
  .app {
    @apply flex flex-col 
    p-0
    items-center justify-center;
    width: 100vw;
    height: 100vh;
    background-color: var(--background-color);
  }
  .sidebar-and-nb {
    @apply flex flex-row 
    w-full h-full p-0 pt-8 pb-5;
  }
</style>
