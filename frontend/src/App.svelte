<script lang="ts">
  import NavBar from "./components/app_components/NavBar.svelte";
  import StatusBar from "./components/app_components/StatusBar.svelte";
  import SideBar from "./components/app_components/SideBar.svelte";
  import Notebook from "./components/nb_components/Notebook.svelte";
</script>

<div class="app">
  <NavBar />
  <div class="sidebar-and-nb">
    <SideBar />
    <Notebook />
  </div>
  <StatusBar />
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
    w-full h-full p-0;
  }
</style>
