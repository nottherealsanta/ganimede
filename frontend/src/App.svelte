<script lang="ts">
  import svelteLogo from "./assets/svelte.svg";
  import ganimedeLogo from "/ganimede.svg";
  import Counter from "./lib/Counter.svelte";
  import NavBar from "./components/app_components/NavBar.svelte";
  import StatusBar from "./components/app_components/StatusBar.svelte";
</script>

<main>
  <NavBar />
  <StatusBar />
  <div>
    <img src={ganimedeLogo} class="logo" alt="Ganimede Logo" />
  </div>
  <h1>Hello</h1>
  <div class="card">
    <Counter />
  </div>
</main>

<style>
</style>
