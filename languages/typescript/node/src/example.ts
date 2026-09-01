/**
 * Example service demonstrating the testable service-layer pattern.
 * Deliberately generic — replace it with your own domain logic.
 */

export class ExampleService {
  #items = new Map<number, string>();
  #nextId = 1;

  create(name: string): { id: number; name: string } {
    const trimmed = name.trim();
    if (!trimmed) {
      throw new Error("name must not be empty");
    }
    const item = { id: this.#nextId, name: trimmed };
    this.#items.set(item.id, item.name);
    this.#nextId += 1;
    return item;
  }

  get(id: number): { id: number; name: string } {
    const name = this.#items.get(id);
    if (name === undefined) {
      throw new Error(`Example ${id} not found`);
    }
    return { id, name };
  }

  list(): Array<{ id: number; name: string }> {
    return [...this.#items.entries()].map(([id, name]) => ({ id, name }));
  }
}
