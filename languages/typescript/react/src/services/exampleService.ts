export interface ExampleItem {
  id: number;
  name: string;
}

/**
 * Example service — framework-free and unit-testable.
 */
export class ExampleService {
  #items = new Map<number, ExampleItem>();
  #nextId = 1;

  create(name: string): ExampleItem {
    const trimmed = name.trim();
    if (!trimmed) {
      throw new Error("name must not be empty");
    }
    const item = { id: this.#nextId++, name: trimmed };
    this.#items.set(item.id, item);
    return item;
  }

  get(id: number): ExampleItem | undefined {
    return this.#items.get(id);
  }

  list(): ExampleItem[] {
    return [...this.#items.values()];
  }
}

export const exampleService = new ExampleService();
