export let config = {};

export async function fetchConfig() {
    const response = await fetch("/config");
    const data = await response.json();
    config = data;
    console.log("config.js: " + JSON.stringify(config));
}

