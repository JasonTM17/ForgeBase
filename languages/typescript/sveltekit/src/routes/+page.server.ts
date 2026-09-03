import { exampleService } from "$lib/exampleService.js";

export function load(): { items: ReturnType<typeof exampleService.list> } {
  return { items: exampleService.list() };
}
