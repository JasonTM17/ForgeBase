import { mount } from "svelte";

import App from "./App.svelte";

const root = document.getElementById("app");
if (!root) throw new Error("Root element #app not found");

// Svelte 5 mount returns a handle; capture it for potential teardown.
const _app: unknown = mount(App, { target: root });
void _app;
