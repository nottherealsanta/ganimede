<script lang="ts">
  import { Folder, File, ChevronLeft, X, Home } from "lucide-svelte";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  let is_open = false;
  let current_path = writable<string>("");
  let contents = writable<{ name: string; type: string }[]>([]);

  function fetch_contents(path: string = "") {
    fetch(`/file_browser?path=${encodeURIComponent(path)}`)
      .then((response) => response.json())
      .then((data) => {
        data.contents.sort(
          (
            a: { name: string; type: string },
            b: { name: string; type: string }
          ) => {
            const aIsIpynb = a.name.endsWith(".ipynb");
            const bIsIpynb = b.name.endsWith(".ipynb");

            // Both are .ipynb files or neither is, sort alphabetically
            if (aIsIpynb === bIsIpynb) {
              if (a.type === b.type) {
                return a.name.localeCompare(b.name);
              }
              // If types are different and one is a folder, it comes first
              return a.type === "folder" ? -1 : 1;
            }

            // If only a is .ipynb, it comes first
            return aIsIpynb ? -1 : 1;
          }
        );
        contents.set(data.contents);
      });
  }

  function navigate_back() {
    current_path.update((path) => {
      const parts = path.split("/").filter(Boolean);
      parts.pop();
      return parts.join("/");
    });
  }

  function open_notebook(notebook_name: string) {
    fetch(
      `/open_notebook?path=${encodeURIComponent($current_path)}/${notebook_name}`
    )
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        is_open = false;
      });
  }

  onMount(() => {
    fetch_contents();
  });

  current_path.subscribe((path) => {
    fetch_contents(path);
  });
</script>

<button
  class="flex flex-col items-center justify-center w-fit h-fit"
  on:click={() => {
    is_open = true;
  }}
>
  Open a notebook
</button>

{#if is_open}
  <div
    class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-25"
    on:click={() => {
      is_open = false;
    }}
  >
    <div
      class="modal"
      on:click={(e) => {
        e.stopPropagation();
      }}
    >
      <!-- Open a Notebook        X -->
      <div
        class="flex w-full bg-gray-50 justify-between items-center py-2 px-4"
      >
        <h1 class="text-xl font-bold">Open a notebook</h1>
        <button
          class="bg-gray-100 py-2 px-2 rounded-full hover:bg-gray-200"
          on:click={() => {
            is_open = false;
          }}
        >
          <X />
        </button>
      </div>

      <div class="flex flex-col w-full h-full px-4 pb-4 pt-2">
        <div class="flex items-center w-full h-12 px-3 py-1">
          <!-- back button -->
          <button
            class="h-10 w-10 mr-2 flex flex-row items-center justify-center rounded-2xl
        {$current_path === ''
              ? 'bg-transparent'
              : 'bg-transparent hover:bg-gray-100'}
        "
            on:click={() => {
              navigate_back();
            }}
            disabled={$current_path === ""}
          >
            {#if $current_path === ""}
              <Home size="18" />
            {:else}
              <ChevronLeft size="18" />
            {/if}
          </button>
          <!-- current path -->
          <p class=" w-auto text-nowrap overflow-hidden">
            {#if $current_path === ""}
              /
            {:else}
              {#each $current_path.split("/") as part, index}
                {index > 0 ? " / " : ""}
                {part}
              {/each}
            {/if}
          </p>
        </div>
        <!-- File/Folder list -->
        <div
          class="flex w-full p-2 flex-col items-start overflow-auto h-full border border-gray-100 ring-2 ring-gray-50 rounded-md"
        >
          {#each $contents as item}
            <button
              class="folder_file {item.type === 'folder'
                ? 'text-gray-700 hover:bg-gray-100'
                : ''}
              {item.type === 'file' && item.name.endsWith('.ipynb')
                ? 'text-blue-500 hover:bg-gray-100'
                : 'text-gray-400'}
              "
              on:click={() => {
                if (item.type === "folder") {
                  current_path.update((path) => `${path}/${item.name}`);
                } else if (item.name.endsWith(".ipynb")) {
                  open_notebook(item.name);
                }
              }}
              disabled={item.type === "file" && !item.name.endsWith(".ipynb")}
              style={item.type === "file" && !item.name.endsWith(".ipynb")
                ? "cursor: not-allowed;"
                : ""}
            >
              <!-- {item.name} ({item.type}) -->
              {#if item.type === "folder"}
                <Folder size="18" class="mr-2" /> {item.name}
              {:else}
                <File size="18" class="mr-2" />
                {item.name}
              {/if}
            </button>
          {/each}
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal {
    @apply h-2/3 w-1/3 flex flex-col items-start;
    background-color: white;
    border-radius: 0.5rem;
    overflow: hidden;
    font-family: "IBM Plex Sans", sans-serif;
    scrollbar-color: #d1d5db #f3f4f6;
  }

  .folder_file {
    @apply flex justify-start items-center w-auto mb-1 px-4 py-1 rounded text-nowrap;
  }
</style>
