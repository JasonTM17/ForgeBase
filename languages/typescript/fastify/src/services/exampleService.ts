import { NotFoundError } from "../errors.js";

export interface Example {
  id: number;
  name: string;
}

export class ExampleService {
  #items = new Map<number, Example>();
  #nextId = 1;
  create(name: string): Example {
    const trimmed = name.trim();
    if (!trimmed) throw new Error("name must not be empty");
    const item: Example = { id: this.#nextId++, name: trimmed };
    this.#items.set(item.id, item);
    return item;
  }
  get(id: number): Example {
    const item = this.#items.get(id);
    if (!item) throw new NotFoundError(`Example ${id} not found`);
    return item;
  }
  list(): Example[] {
    return [...this.#items.values()];
  }
  reset(): void {
    this.#items.clear();
    this.#nextId = 1;
  }
}
export const exampleService = new ExampleService();
