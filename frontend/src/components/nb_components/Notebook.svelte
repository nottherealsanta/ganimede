<script lang="ts">
  import Cell from "../cell_components/Cell.svelte";
</script>

<div class="nb">
  <Cell />
</div>

<style>
  .nb {
    @apply flex
    flex-col
    w-full h-full px-8 pt-8
    bg-transparent;
    min-width: 500px;
  }
</style>
