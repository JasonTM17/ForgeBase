export interface ExampleItem {
  id: number;
  name: string;
}

export class ExampleService {
  #items = new Map<number, ExampleItem>();
  #nextId = 1;
  create(name: string): ExampleItem {
    const t = name.trim();
    if (!t) throw new Error("name must not be empty");
    const item = { id: this.#nextId++, name: t };
    this.#items.set(item.id, item);
    return item;
  }
  list(): ExampleItem[] {
    return [...this.#items.values()];
  }
}
export const exampleService = new ExampleService();
