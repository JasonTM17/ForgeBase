import { defineComponent, h, onErrorCaptured, ref, type Ref } from "vue";

import { exampleService, type ExampleItem } from "./services/exampleService.js";

/**
 * App-level error handler — Vue's onErrorCaptured keeps a component crash from
 * blanking the whole tree. In production, report to your error tracker.
 */
export function useErrorHandler(): Ref<string | null> {
  const error = ref<string | null>(null);
  onErrorCaptured((err: unknown) => {
    error.value = err instanceof Error ? err.message : String(err);
    console.error("[error]", err);
    return false; // don't propagate further
  });
  return error;
}

export default defineComponent({
  name: "App",
  setup() {
    const error = useErrorHandler();
    const items: Ref<ExampleItem[]> = ref(exampleService.list());

    function add(): void {
      const name = window.prompt("Name?");
      if (name && name.trim()) {
        exampleService.create(name);
        items.value = exampleService.list();
      }
    }

    return () =>
      error.value
        ? h("div", { role: "alert" }, [h("h1", "Something went wrong"), h("pre", error.value)])
        : h("main", [
            h("h1", "ForgeBase Vue Starter"),
            h("section", [
              h("h2", "Examples"),
              h("button", { type: "button", onClick: add }, "Add"),
              h(
                "ul",
                items.value.map((i) => h("li", { key: i.id }, `${i.id}: ${i.name}`)),
              ),
            ]),
          ]);
  },
});
